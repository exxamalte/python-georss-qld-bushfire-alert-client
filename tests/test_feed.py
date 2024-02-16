"""Test for the Queensland Bushfire Alert feed."""
import datetime
from unittest import mock

import pytest
from georss_client import UPDATE_OK

from georss_qld_bushfire_alert_client.feed import QldBushfireAlertFeed
from tests.utils import load_fixture

HOME_COORDINATES = (-31.0, 151.0)


@mock.patch("requests.Request")
@mock.patch("requests.Session")
def test_update_ok(mock_session, mock_request):
    """Test updating feed is ok."""
    mock_session.return_value.__enter__.return_value.send.return_value.ok = True
    mock_session.return_value.__enter__.return_value.send.return_value.text = (
        load_fixture("qld_bushfire_alert_feed.xml")
    )

    feed = QldBushfireAlertFeed(HOME_COORDINATES)
    assert (
        repr(feed) == "<QldBushfireAlertFeed(home=(-31.0, 151.0), "
        "url=https://www.qfes.qld.gov.au/data/alerts/"
        "bushfireAlert.xml, radius=None, categories="
        "None)>"
    )
    status, entries = feed.update()
    assert status == UPDATE_OK
    assert entries is not None
    assert len(entries) == 2

    feed_entry = entries[0]
    assert feed_entry.title == "Title 1"
    assert feed_entry.external_id == "1234"
    assert feed_entry.coordinates == (-32.2345, 149.1234)
    assert feed_entry.distance_to_home == pytest.approx(224.5, 0.1)
    assert feed_entry.published == datetime.datetime(2018, 9, 27, 8, 0)
    assert feed_entry.updated == datetime.datetime(2018, 9, 27, 8, 30)
    assert feed_entry.status == "Status 1"
    assert feed_entry.attribution == "Author 1"
    assert repr(feed_entry) == "<QldBushfireAlertFeedEntry(id=1234)>"

    feed_entry = entries[1]
    assert feed_entry.title == "Title 2"
    assert feed_entry.published is None
    assert feed_entry.updated is None


@mock.patch("requests.Request")
@mock.patch("requests.Session")
def test_update_ok_with_category(mock_session, mock_request):
    """Test updating feed is ok."""
    mock_session.return_value.__enter__.return_value.send.return_value.ok = True
    mock_session.return_value.__enter__.return_value.send.return_value.text = (
        load_fixture("qld_bushfire_alert_feed.xml")
    )

    feed = QldBushfireAlertFeed(HOME_COORDINATES, filter_categories=["Category 1"])
    status, entries = feed.update()
    assert status == UPDATE_OK
    assert entries is not None
    assert len(entries) == 1

    feed_entry = entries[0]
    assert feed_entry.title == "Title 1"
    assert feed_entry.external_id == "1234"
