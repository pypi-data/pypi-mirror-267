r"""
                                                             
 _______  _______         _______  _______  _______  _______  _______  _______  _______ 
(  ___  )(  ____ \       (  ____ \(  ____ \(  ____ )(  ___  )(  ____ )(  ____ \(  ____ )
| (   ) || (    \/       | (    \/| (    \/| (    )|| (   ) || (    )|| (    \/| (    )|
| |   | || (__     _____ | (_____ | |      | (____)|| (___) || (____)|| (__    | (____)|
| |   | ||  __)   (_____)(_____  )| |      |     __)|  ___  ||  _____)|  __)   |     __)
| |   | || (                   ) || |      | (\ (   | (   ) || (      | (      | (\ (   
| (___) || )             /\____) || (____/\| ) \ \__| )   ( || )      | (____/\| ) \ \__
(_______)|/              \_______)(_______/|/   \__/|/     \||/       (_______/|/   \__/
                                                                                      
"""
import asyncio
import contextvars
import logging
import traceback
from concurrent.futures import ThreadPoolExecutor

import arrow
from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.style import Style
from tenacity import (
    AsyncRetrying,
    retry,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_random,
)

import ofscraper.classes.sessionbuilder as sessionbuilder
import ofscraper.db.operations as operations
import ofscraper.utils.args.read as read_args
import ofscraper.utils.cache as cache
import ofscraper.utils.config.data as data
import ofscraper.utils.console as console
import ofscraper.utils.constants as constants
from ofscraper.classes.semaphoreDelayed import semaphoreDelayed
from ofscraper.utils.context.run_async import run

log = logging.getLogger("shared")
attempt = contextvars.ContextVar("attempt")
sem = None


@run
async def get_messages(model_id, username, forced_after=None):
    global sem
    sem = semaphoreDelayed(constants.getattr("MAX_SEMAPHORE"))
    with ThreadPoolExecutor(
        max_workers=constants.getattr("MAX_REQUEST_WORKERS")
    ) as executor:
        asyncio.get_event_loop().set_default_executor(executor)
        overall_progress = Progress(
            SpinnerColumn(
                style=Style(color="blue"),
            ),
            TextColumn("Getting Messages...\n{task.description}"),
        )
        job_progress = Progress("{task.description}")
        progress_group = Group(overall_progress, Panel(Group(job_progress)))
        global tasks
        global after
        global new_tasks

        new_tasks = []
        tasks = []
        responseArray = []
        page_count = 0
        # require a min num of posts to be returned
        min_posts = 50
        with Live(
            progress_group,
            refresh_per_second=constants.getattr("refreshScreen"),
            console=console.get_shared_console(),
        ):
            async with sessionbuilder.sessionBuilder() as c:
                oldmessages = (
                    operations.get_messages_data(model_id=model_id, username=username)
                    if not read_args.retriveArgs().no_cache
                    else []
                )
                log.trace(
                    "oldmessage {posts}".format(
                        posts="\n\n".join(
                            list(map(lambda x: f"oldmessages: {str(x)}", oldmessages))
                        )
                    )
                )
                oldmessages = list(
                    filter(lambda x: (x.get("date")) != None, oldmessages)
                )
                log.debug(f"[bold]Messages Cache[/bold] {len(oldmessages)} found")

                oldmessages = sorted(
                    oldmessages,
                    key=lambda x: arrow.get(x.get("date")).float_timestamp,
                    reverse=True,
                )
                oldmessages = [
                    {"date": arrow.now().float_timestamp, "id": None}
                ] + oldmessages

                before = (read_args.retriveArgs().before or arrow.now()).float_timestamp
                after = get_after(model_id, username, forced_after)

                log.debug(f"Messages after = {after}")

                log.debug(f"Messages before = {before}")

                if after > before:
                    return []
                elif len(oldmessages) <= 2:
                    filteredArray = oldmessages
                else:
                    filteredArray = oldmessages[
                        get_i(oldmessages, before) : get_j(oldmessages, after)
                    ]
                log.info(
                    f"""
Setting initial message scan date for {username} to {arrow.get(after).format('YYYY.MM.DD')}
[yellow]Hint: append ' --after 2000' to command to force scan of all messages + download of new files only[/yellow]
[yellow]Hint: append ' --after 2000 --dupe' to command to force scan of all messages + download/re-download of all files[/yellow]

                """
                )

                splitArrays = [
                    filteredArray[i : i + min_posts]
                    for i in range(0, len(filteredArray), min_posts)
                ]
                if len(splitArrays) > 2:
                    tasks.append(
                        asyncio.create_task(
                            scrape_messages(
                                c,
                                model_id,
                                progress=job_progress,
                                message_id=splitArrays[0][0].get("id")
                                if len(filteredArray) == len(oldmessages)
                                else None,
                                required_ids=set(
                                    [ele.get("date") for ele in splitArrays[0]]
                                ),
                            )
                        )
                    )
                    [
                        tasks.append(
                            asyncio.create_task(
                                scrape_messages(
                                    c,
                                    model_id,
                                    progress=job_progress,
                                    message_id=splitArrays[i - 1][-1].get("id"),
                                    required_ids=set(
                                        [ele.get("date") for ele in splitArrays[i]]
                                    ),
                                )
                            )
                        )
                        for i in range(1, len(splitArrays) - 1)
                    ]
                    # keeping grabbing until nothing left
                    tasks.append(
                        asyncio.create_task(
                            scrape_messages(
                                c,
                                model_id,
                                progress=job_progress,
                                message_id=splitArrays[-2][-1].get("id"),
                                required_ids=set(
                                    [ele.get("date") for ele in splitArrays[-1]]
                                ),
                            )
                        )
                    )
                # use the first split if less then 3
                elif len(splitArrays) > 0:
                    tasks.append(
                        asyncio.create_task(
                            scrape_messages(
                                c,
                                model_id,
                                progress=job_progress,
                                required_ids=None,
                                message_id=splitArrays[0][0].get("id")
                                if len(filteredArray) == len(oldmessages)
                                else None,
                            )
                        )
                    )
                # set init message to none
                else:
                    tasks.append(
                        asyncio.create_task(
                            scrape_messages(
                                c,
                                model_id,
                                progress=job_progress,
                                message_id=None,
                                required_ids=None,
                            )
                        )
                    )

                page_task = overall_progress.add_task(
                    f" Pages Progress: {page_count}", visible=True
                )

                while tasks:
                    done, pending = await asyncio.wait(
                        tasks, return_when=asyncio.FIRST_COMPLETED
                    )
                    for result in done:
                        try:
                            out = await result
                        except Exception as E:
                            log.debug(E)
                            continue
                        page_count = page_count + 1
                        overall_progress.update(
                            page_task, description=f"Pages Progress: {page_count}"
                        )
                        responseArray.extend(out)
                    tasks = list(pending)
                    tasks.extend(new_tasks)
                    new_tasks = []
                overall_progress.remove_task(page_task)

        unduped = {}
        log.debug(f"[bold]Messages Count with Dupes[/bold] {len(responseArray)} found")

        for message in responseArray:
            id = message["id"]
            if unduped.get(id):
                continue
            unduped[id] = message

        log.trace(f"messages dupeset messageids {unduped.keys()}")
        log.trace(
            "messages raw unduped {posts}".format(
                posts="\n\n".join(
                    list(map(lambda x: f"undupedinfo message: {str(x)}", unduped))
                )
            )
        )
        set_check(unduped, model_id, after)
        return list(unduped.values())


def get_i(oldmessages, before):
    """
    iterate through posts until a date less then or equal
    to before , set index to -1 this point
    """
    if before >= oldmessages[1].get("date"):
        return 0
    if before <= oldmessages[-1].get("date"):
        return len(oldmessages) - 2
    # Use a generator expression for efficiency
    return max(
        next(
            index - 1
            for index, message in enumerate(oldmessages)
            if message.get("date") <= before
        ),
        0,
    )


def get_j(oldmessages, after):
    """
    iterate through posts until a date less then or equal
    to after , set index to +1 this point
    """
    after=after-1000
    if after >= oldmessages[0].get("date"):
        return 0
    if after < oldmessages[-1].get("date"):
        return len(oldmessages) - 1
    return min(
        next(
            index + 1
            for index, message in enumerate(oldmessages)
            if message.get("date") <= after
        ),
        len(oldmessages) - 1,
    )


def set_check(unduped, model_id, after):
    if not after:
        newCheck = {}
        for post in cache.get(f"message_check_{model_id}", default=[]) + list(
            unduped.values()
        ):
            newCheck[post["id"]] = post
        cache.set(
            f"message_check_{model_id}",
            list(newCheck.values()),
            expire=constants.getattr("DAY_SECONDS"),
        )
        cache.close()


async def scrape_messages(
    c, model_id, progress, message_id=None, required_ids=None
) -> list:
    global sem
    global tasks
    messages = None
    attempt.set(0)
    ep = (
        constants.getattr("messagesNextEP")
        if message_id
        else constants.getattr("messagesEP")
    )
    url = ep.format(model_id, message_id)
    log.debug(f"{message_id if message_id else 'init'}{url}")
    async for _ in AsyncRetrying(
        retry=retry_if_not_exception_type(KeyboardInterrupt),
        stop=stop_after_attempt(constants.getattr("NUM_TRIES")),
        wait=wait_random(
            min=constants.getattr("OF_MIN"),
            max=constants.getattr("OF_MAX"),
        ),
        reraise=True,
    ):
        with _:
            await sem.acquire()
            try:
                async with c.requests(url=url)() as r:
                    attempt.set(attempt.get(0) + 1)

                    task = progress.add_task(
                        f"Attempt {attempt.get()}/{constants.getattr('NUM_TRIES')}: Message ID-> {message_id if message_id else 'initial'}"
                    )
                    if r.ok:
                        messages = (await r.json_())["list"]
                        log_id = f"offset messageid:{message_id if message_id else 'init id'}"
                        if not messages:
                            messages = []
                        if len(messages) == 0:
                            log.debug(f"{log_id} -> number of messages found 0")
                        elif len(messages) > 0:
                            log.debug(
                                f"{log_id} -> number of messages found {len(messages)}"
                            )
                            log.debug(
                                f"{log_id} -> first date {messages[-1].get('createdAt') or messages[0].get('postedAt')}"
                            )
                            log.debug(
                                f"{log_id} -> last date {messages[-1].get('createdAt') or messages[0].get('postedAt')}"
                            )
                            log.debug(
                                f"{log_id} -> found message ids {list(map(lambda x:x.get('id'),messages))}"
                            )
                            log.trace(
                                "{log_id} -> messages raw {posts}".format(
                                    log_id=log_id,
                                    posts="\n\n".join(
                                        list(
                                            map(
                                                lambda x: f" messages scrapeinfo: {str(x)}",
                                                messages,
                                            )
                                        )
                                    ),
                                )
                            )
                            timestamp = arrow.get(
                                messages[-1].get("createdAt")
                                or messages[-1].get("postedAt")
                            ).float_timestamp

                            if timestamp < after:
                                attempt.set(0)
                            elif required_ids == None:
                                attempt.set(0)
                                new_tasks.append(
                                    asyncio.create_task(
                                        scrape_messages(
                                            c,
                                            model_id,
                                            progress,
                                            message_id=messages[-1]["id"],
                                        )
                                    )
                                )
                            else:
                                [
                                    required_ids.discard(
                                        ele.get("createdAt") or ele.get("postedAt")
                                    )
                                    for ele in messages
                                ]

                                if len(required_ids) > 0 and timestamp > min(
                                    list(required_ids)
                                ):
                                    attempt.set(0)
                                    new_tasks.append(
                                        asyncio.create_task(
                                            scrape_messages(
                                                c,
                                                model_id,
                                                progress,
                                                message_id=messages[-1]["id"],
                                                required_ids=required_ids,
                                            )
                                        )
                                    )

                    else:
                        log.debug(
                            f"[bold]message response status code:[/bold]{r.status}"
                        )
                        log.debug(f"[bold]message response:[/bold] {await r.text_()}")
                        log.debug(f"[bold]message headers:[/bold] {r.headers}")

                        r.raise_for_status()
            except Exception as E:
                log.traceback_(E)
                log.traceback_(traceback.format_exc())
                raise E
            finally:
                sem.release()
                progress.remove_task(task)
            return messages


def get_individual_post(model_id, postid, c=None):
    with c.requests(
        url=constants.getattr("messageSPECIFIC").format(model_id, postid)
    )() as r:
        if r.ok:
            log.trace(f"message raw individual {r.json()}")
            return r.json()["list"][0]
        else:
            log.debug(
                f"[bold]Individual message response status code:[/bold]{r.status}"
            )
            log.debug(f"[bold]Individual message  response:[/bold] {r.text_()}")
            log.debug(f"[bold]Individual message  headers:[/bold] {r.headers}")


def get_after(model_id, username, forced_after=None):
    if forced_after != None:
        return forced_after
    elif read_args.retriveArgs().after == 0:
        return 0
    elif read_args.retriveArgs().after:
        return read_args.retriveArgs().after.float_timestamp
    elif (
        cache.get("{model_id}_scrape_messages")
        and not read_args.retriveArgs().after
        and not data.get_disable_after()
    ):
        log.debug(
            "Used --after previously. Scraping all messages required to make sure content is not missing"
        )
        return 0
    curr = operations.get_messages_media(model_id=model_id, username=username)
    if len(curr) == 0:
        log.debug("Setting date to zero because database is empty")
        return 0
    missing_items = list(filter(lambda x: x[10] != 1, curr))
    missing_items = list(sorted(missing_items, key=lambda x: arrow.get(x[11])))
    if len(missing_items) == 0:
        log.debug(
            "Using last db date because,all downloads in db are marked as downloaded"
        )
        return operations.get_last_message_date(model_id=model_id, username=username)
    else:
        log.debug(
            f"Setting date slightly before earliest missing item\nbecause {len(missing_items)} messages in db are marked as undownloaded"
        )
        return arrow.get(missing_items[0][11]).float_timestamp
