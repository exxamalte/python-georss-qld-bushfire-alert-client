# python-georss-qld-bushfire-alert-client

[![Build Status](https://img.shields.io/github/actions/workflow/status/exxamalte/python-georss-qld-bushfire-alert-client/ci.yaml)](https://github.com/exxamalte/python-georss-qld-bushfire-alert-client/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/gh/exxamalte/python-georss-qld-bushfire-alert-client/branch/master/graph/badge.svg?token=0YWR76U4GN)](https://codecov.io/gh/exxamalte/python-georss-qld-bushfire-alert-client)
[![PyPi](https://img.shields.io/pypi/v/georss-qld-bushfire-alert-client.svg)](https://pypi.python.org/pypi/georss-qld-bushfire-alert-client)
[![Version](https://img.shields.io/pypi/pyversions/georss-qld-bushfire-alert-client.svg)](https://pypi.python.org/pypi/georss-qld-bushfire-alert-client)

This library provides convenient access to the [Queensland Bushfire Alert Feed](https://www.ruralfire.qld.gov.au/map/Pages/default.aspx).

## Installation
`pip install georss-qld-bushfire-alert-client`

## Usage
See below for an example of how this library can be used. After instantiating 
the feed class and supplying the required parameters, you can call `update` to 
retrieve the feed data. The return value will be a tuple of a status code and 
the actual data in the form of a list of specific feed entries.

**Status Codes**
* _UPDATE_OK_: Update went fine and data was retrieved. The library may still return empty data, for example because no entries fulfilled the filter criteria.
* _UPDATE_OK_NO_DATA_: Update went fine but no data was retrieved, for example because the server indicated that there was not update since the last request.
* _UPDATE_ERROR_: Something went wrong during the update


**Supported Filters**

| Filter     |                     | Description |
|------------|---------------------|-------------|
| Radius     | `filter_radius`     | Radius in kilometers around the home coordinates in which events from the feed are included. |
| Categories | `filter_categories` | Array of category names. Only events with a category matching any of these are included. |

**Example**
```python
from georss_qld_bushfire_alert_client import QldBushfireAlertFeed
# Home Coordinates: Latitude: -27.5, Longitude: 153.0
# Filter radius: 50 km
# Filter categories: 'Advice'
feed = QldBushfireAlertFeed((-27.5, 153.0), 
                            filter_radius=50, 
                            filter_categories=['Advice'])
status, entries = feed.update()
```

## Feed entry properties
Each feed entry is populated with the following properties - subject to 
availability in GeoRSS feed:

| Name             | Description                                               |
|------------------|-----------------------------------------------------------|
| geometry         | All geometry details of this entry.                       |
| coordinates      | Best coordinates (latitude, longitude) of this entry.     |
| external_id      | External id of this entry.                                |
| title            | Title of this entry with textual description of location. |
| category         | Category of this entry.                                   |
| attribution      | Attribution from feed.                                    |
| distance_to_home | Distance in km of this entry to the home coordinates.     |
| description      | Full content of this entry.                               |
| published        | Published date of this entry.                             |
| updated          | Updated date of this entry.                               |
| status           | Status of alert, e.g. "Patrolled", "Going", "Contained"   |

## Feed Manager
The Feed Manager helps managing feed updates over time, by notifying the 
consumer of the feed about new feed entries, updates and removed entries 
compared to the last feed update.

* If the current feed update is the first one, then all feed entries will be 
  reported as new. The feed manager will keep track of all feed entries' 
  external IDs that it has successfully processed.
* If the current feed update is not the first one, then the feed manager will 
  produce three sets:
  * Feed entries that were not in the previous feed update but are in the 
    current feed update will be reported as new.
  * Feed entries that were in the previous feed update and are still in the 
    current feed update will be reported as to be updated.
  * Feed entries that were in the previous feed update but are not in the 
    current feed update will be reported to be removed.
* If the current update fails, then all feed entries processed in the previous
  feed update will be reported to be removed.

After a successful update from the feed, the feed manager will provide two
different dates:

* `last_update` will be the timestamp of the last successful update from the
  feed. This date may be useful if the consumer of this library wants to
  treat intermittent errors from feed updates differently.
* `last_timestamp` will be the latest timestamp extracted from the feed data. 
  This requires that the underlying feed data actually contains a suitable 
  date. This date may be useful if the consumer of this library wants to 
  process feed entries differently if they haven't actually been updated.
