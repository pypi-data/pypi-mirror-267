mediaCreate = """
CREATE TABLE IF NOT EXISTS medias (
	id INTEGER NOT NULL, 
	media_id INTEGER, 
	post_id INTEGER NOT NULL, 
	link VARCHAR, 
	directory VARCHAR, 
	filename VARCHAR, 
	size INTEGER, 
	api_type VARCHAR, 
	media_type VARCHAR, 
	preview INTEGER, 
	linked VARCHAR, 
	downloaded INTEGER, 
	created_at TIMESTAMP, 
	hash VARCHAR,
	PRIMARY KEY (id), 
	UNIQUE (media_id)
);"""

messagesCreate = """
CREATE TABLE IF NOT EXISTS messages (
	id INTEGER NOT NULL, 
	post_id INTEGER NOT NULL, 
	text VARCHAR, 
	price INTEGER, 
	paid INTEGER, 
	archived BOOLEAN, 
	created_at TIMESTAMP, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (post_id)
)
"""
postCreate = """
CREATE TABLE IF NOT EXISTS posts (
	id INTEGER NOT NULL, 
	post_id INTEGER NOT NULL, 
	text VARCHAR, 
	price INTEGER, 
	paid INTEGER, 
	archived BOOLEAN, 
	created_at TIMESTAMP, 
	PRIMARY KEY (id), 
	UNIQUE (post_id)
)
"""
otherCreate = """
CREATE TABLE IF NOT EXISTS others (
	id INTEGER NOT NULL,  
	post_id INTEGER NOT NULL, 
	text VARCHAR, 
	price INTEGER, 
	paid INTEGER, 
	archived BOOLEAN, 
	created_at TIMESTAMP, 
	PRIMARY KEY (id), 
	UNIQUE (post_id)
)
"""
productCreate = """
CREATE TABLE IF NOT EXISTS products (
	id INTEGER NOT NULL, 
	post_id INTEGER NOT NULL, 
	text VARCHAR, 
	price INTEGER, 
	paid INTEGER, 
	archived BOOLEAN, 
	created_at TIMESTAMP, title VARCHAR, 
	PRIMARY KEY (id), 
	UNIQUE (post_id)
)
"""
profilesCreate = """
CREATE TABLE IF NOT EXISTS profiles (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	username VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username)
)
"""

storiesCreate = """
CREATE TABLE IF NOT EXISTS stories (
	id INTEGER NOT NULL, 
	post_id INTEGER NOT NULL, 
	text VARCHAR, 
	price INTEGER, 
	paid INTEGER, 
	archived BOOLEAN, 
	created_at TIMESTAMP, 
	PRIMARY KEY (id), 
	UNIQUE (post_id)
)
"""

messagesInsert = f"""INSERT INTO 'messages'(
post_id, text,price,paid,archived,
created_at,user_id)
            VALUES (?, ?,?,?,?,?,?);"""


postInsert = f"""INSERT INTO 'posts'(
post_id, text,price,paid,archived,
created_at)
            VALUES (?, ?,?,?,?,?);"""


postNormalCheck = """
SELECT post_id FROM posts where archived=False
"""

storiesInsert = f"""INSERT INTO 'stories'(
post_id, text,price,paid,archived,
created_at)
            VALUES (?, ?,?,?,?,?);"""


allIDCheck = """
SELECT media_id FROM medias
"""

allDLIDCheck = """
SELECT media_id FROM medias where downloaded=(1)
"""

allPOSTCheck = """
SELECT post_id FROM posts
"""

allMessagesCheck = """
SELECT post_id FROM messages
"""

allStoriesCheck = """
SELECT post_id FROM stories
"""

mediaInsert = f"""INSERT INTO 'medias'(
media_id,post_id,link,directory,filename,size,api_type,media_type,preview,linked,downloaded,created_at,hash)
            VALUES (?, ?,?,?,?,?,?,?,?,?,?,?,?);"""

mediaDupeCheck = """
SELECT media_id,post_id,link,directory,filename,size
,api_type,media_type ,preview,linked,downloaded,created_at,
hash
FROM medias where media_id=(?)
"""


getTimelineMedia = """
SELECT media_id,post_id,link,directory,filename,size
,api_type,media_type ,preview,linked,downloaded,created_at,
hash
FROM medias where api_type=('Timeline')
"""

getArchivedMedia = """
SELECT media_id,post_id,link,directory,filename,size
,api_type,media_type ,preview,linked,downloaded,created_at,
hash
FROM medias where api_type=('Archived')
"""

getMessagesMedia = """
SELECT media_id,post_id,link,directory,filename,size
,api_type,media_type ,preview,linked,downloaded,created_at,
hash
FROM medias where api_type=('Message') or api_type=('Messages')
"""

mediaUpdate = f"""Update 'medias'
SET
media_id=?,post_id=?,link=?,directory=?,filename=?,size=?,
api_type=?,media_type=?,preview=?,linked=?,downloaded=?,created_at=?,hash=?
WHERE media_id=(?);"""

mediaTypeUpdate = f"""Update 'medias'
SET
api_type=?,media_type=?
WHERE media_id=(?);"""

profileTableCheck = """
SELECT name FROM sqlite_master WHERE type='table' AND name='profiles';
"""

profileInsert = f"""INSERT INTO 'profiles'(
user_id,username)
            VALUES (?, ?);"""


profileUpdate = f"""Update 'profiles'
SET
user_id=?,username=?
WHERE user_id=(?);"""

profileDupeCheck = """
SELECT * FROM profiles where user_id=(?)
"""

labelsCreate = """
CREATE TABLE IF NOT EXISTS labels (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	type VARCHAR, 
	post_id INTEGER, 
	PRIMARY KEY (id, post_id)
)
"""


labelInsert = f"""INSERT INTO 'labels'(
id, name, type, post_id)
VALUES (?, ?,?,?);"""


labelInsert2 = f"""INSERT INTO 'labels'(
label_id, name, type, post_id)
VALUES (?, ?,?,?);"""

labelID = """
SELECT id,post_id  FROM  labels
"""

timelinePostInfo = """
SELECT created_at,post_id FROM posts where archived=(0)
"""
archivedPostInfo = """
SELECT created_at,post_id FROM posts where archived=(1)
"""

messagesData = """
SELECT created_at,post_id FROM messages
"""

mediaAddColumn = """
ALTER TABLE medias ADD COLUMN hash VARCHAR;
"""

mediaDupeHashesMedia = """
WITH x AS (
    SELECT hash, size
    FROM medias
    WHERE hash IS NOT NULL AND size is not null and  WHERE hash IS NOT NULL AND size IS NOT NULL AND (media_type = ?)
)
)
SELECT hash
FROM x
GROUP BY hash, size
HAVING COUNT(*) > 1;
"""

mediaDupeHashes = """
WITH x AS (
    SELECT hash, size
    FROM medias
    WHERE hash IS NOT NULL AND size is not null and  WHERE hash IS NOT NULL AND size IS NOT NULL
)
)
SELECT hash
FROM x
GROUP BY hash, size
HAVING COUNT(*) > 1;
"""

mediaDupeFiles = """
SELECT filename
FROM medias
where hash=(?)
"""
