
# 📘 HoloAPI Documentation

HoloAPI is designed to provide a queryable API for fields commonly available in yt-dlp's info.json files.

## 📄 Common Query Parameters

All endpoints support:

| Parameter    | Type   | Description                                |
| ------------ | ------ | ------------------------------------------ |
| `page`       | int    | Page number (default: `1`)                 |
| `per_page`   | int    | Number of results per page (max: `100`)    |
| `sort_by`    | string | Field to sort by (default: `last_updated`) |
| `sort_order` | string | `asc` or `desc` (default: `desc`)          |
| Filtering    |        | See [Filtering](#🔍-filtering) below       |

---

## 📄 Common Fields

These fields are common to most endpoints:

| Parameter      | Type   | Description                                                                        |
| -------------- | ------ | ---------------------------------------------------------------------------------- |
| `created_at`   | string | When the item was first added                                      |
| `last_updated` | string | Last update timestamp for the item. May not represent the latest data scrape time. |

---

## 📦 Endpoints

### `GET /api/channel`

Retrieve paginated list of channels.

**Example:**

```
GET /api/channel?page=1&per_page=10&channel_name__like=Mumei
```

**Fields:**

| Parameter                | Type   | Description                        |
| ------------------------ | ------ | ---------------------------------- |
| `channel_id`             | string | Unique channel identifier          |
| `channel_name`           | string | Name of the channel                |
| `channel_url`            | string | URL of the channel                 |
| `channel_follower_count` | int    | Number of followers (if available) |
| `uploader`               | string | Name of the uploader               |
| `uploader_id`            | string | Uploader's account ID              |
| `uploader_url`           | string | Link to the uploader's page        |

---

### `GET /api/format`

Retrieve available video formats.

**Example:**

```
GET /api/format?resolution__eq=1920x1080&sort_by=created_at&sort_order=desc
```

**Fields:**

| Parameter       | Type     | Description                              |
| --------------- | -------- | ---------------------------------------- |
| `format`        | string   | Format ID (primary key, e.g. "251")      |
| `format_id`     | string   | Format's internal ID                     |
| `format_note`   | string   | Description (e.g. "1080p", "best audio") |
| `resolution`    | string   | Display resolution (e.g. "1920x1080")    |
| `width`         | int      | Width in pixels                          |
| `height`        | int      | Height in pixels                         |
| `fps`           | float    | Frames per second                        |
| `vcodec`        | string   | Video codec used                         |
| `acodec`        | string   | Audio codec used                         |
| `ext`           | string   | File extension                           |
| `protocol`      | string   | Streaming or download protocol           |
| `dynamic_range` | string   | Dynamic range (e.g. "SDR", "HDR")        |
| `quality`       | int      | yt-dlp assigned quality score            |

---

### `GET /api/video`

Retrieve videos with filtering and sorting options.

**Example:**

```
GET /api/video?channel_id=UC1234&live_status__eq=live&page=1
```

**Fields:**

| Parameter            | Type     | Description                             |
| -------------------- | -------- | --------------------------------------- |
| `id`                 | string   | Video ID                                |
| `title`              | string   | Title of the video                      |
| `description`        | string   | Video description                       |
| `channel_id`         | string   | Channel ID where video was uploaded                  |
| `channel_name`       | string   | Name of the channel                     |
| `view_count`         | int      | View count at info.json creation                             |
| `like_count`         | int      | Likes count at info.json creation                             |
| `age_limit`          | int      | Age restriction, where value is minimum age requirement                         |
| `upload_date`        | date     | Upload date (e.g. scheduled stream time)                             |
| `release_date`       | date     | Date of release (if different)          |
| `release_year`       | int      | Year of release                         |
| `timestamp`          | datetime | Internal scrape or event timestamp      |
| `release_timestamp`  | datetime | Exact release timestamp                 |
| `webpage_url`        | string   | URL to the video                        |
| `live_status`        | string   | Live status (e.g. "live", "was\_live", "post\_live") at creation of info.json |
| `media_type`         | string   | Type of video. Currently appears to indicate if livestream or not.                         |
| `is_live`            | bool     | If currently live at creation of info.json                       |
| `was_live`           | bool     | If it was live previously               |
| `availability`       | string   | Visibility status                       |
| `publicly_available` | bool     | True if video is public                 |

---

### `GET /api/thumbnail`

Retrieve video thumbnails.

**Example:**

```
GET /api/thumbnail?resolution__like=720
```

**Fields:**

| Parameter      | Type   | Description                           |
| -------------- | ------ | ------------------------------------- |
| `thumbnail_id` | string | Internal ID for thumbnail             |
| `video_id`     | string | ID of associated video                |
| `url`          | string | URL to the image                      |
| `ext`          | string   | File extension                      |
| `width`        | int    | Width of the image                    |
| `height`       | int    | Height of the image                   |
| `resolution`   | string | Resolution (e.g. "1280x720")          |
| `preference`   | int    | Preference ranking of this thumbnail when info.json was created |

---

### `GET /api/video_format/<video_id>`

Retrieve formats available for a given video, with embedded format details.

**Example:**

```
GET /api/video_format/abc123
```

**Fields:**

| Parameter             | Type   | Description                         |
| --------------------- | ------ | ----------------------------------- |
| `video_id`            | string | ID of the video                     |
| `format`              | string | Format name (foreign key to format) |
| `quality`             | int    | Quality ranking                     |
| `source_preperence`   | int    | yt-dlp preference score when info.json was created        |
| `language_preference` | int    | Language match preference           |
| `format_details`      | object | Full embedded object from `/api/format` |

---

## 🔍 Filtering

You can filter by any valid column using these suffixes:

| Suffix   | Meaning                |
| -------- | ---------------------- |
| `__eq`   | Equals (default)       |
| `__neq`  | Not equals             |
| `__lt`   | Less than              |
| `__lte`  | Less than or equal     |
| `__gt`   | Greater than           |
| `__gte`  | Greater than or equal  |
| `__like` | Case-insensitive match |

**Examples:**

* `channel_name__like=saba`
* `view_count__gte=10000`
* `live_status=live`
* `publicly_available__eq=true`

If no suffix is specified, `__eq` is assumed.

---


