"""Test for the Queensland Bushfire Alert feed manager."""

import datetime
from unittest import mock

from georss_qld_bushfire_alert_client.feed_manager import QldBushfireAlertFeedManager
from tests.utils import load_fixture

HOME_COORDINATES = (-31.0, 151.0)


@mock.patch("requests.Request")
@mock.patch("requests.Session")
def test_feed_manager(mock_session, mock_request):
    """Test the feed manager."""
    mock_session.return_value.__enter__.return_value.send.return_value.ok = True
    mock_session.return_value.__enter__.return_value.send.return_value.text = (
        load_fixture("qld_bushfire_alert_feed.xml")
    )

    # This will just record calls and keep track of external ids.
    generated_entity_external_ids = []
    updated_entity_external_ids = []
    removed_entity_external_ids = []

    def _generate_entity(external_id):
        """Generate new entity."""
        generated_entity_external_ids.append(external_id)

    def _update_entity(external_id):
        """Update entity."""
        updated_entity_external_ids.append(external_id)

    def _remove_entity(external_id):
        """Remove entity."""
        removed_entity_external_ids.append(external_id)

    feed_manager = QldBushfireAlertFeedManager(
        _generate_entity, _update_entity, _remove_entity, HOME_COORDINATES
    )
    assert (
        repr(feed_manager) == "<QldBushfireAlertFeedManager("
        "feed=<QldBushfireAlertFeed(home="
        "(-31.0, 151.0), url=https://publiccontent-gis-psba-qld-gov-au.s3.amazonaws.com/"
        "content/Feeds/BushfireCurrentIncidents/bushfireAlert.xml, "
        "radius=None, categories=None)>)>"
    )
    feed_manager.update()
    entries = feed_manager.feed_entries
    assert entries is not None
    assert len(entries) == 2
    assert feed_manager.last_timestamp == datetime.datetime(2018, 9, 27, 8, 0)
    assert len(generated_entity_external_ids) == 2
    assert len(updated_entity_external_ids) == 0
    assert len(removed_entity_external_ids) == 0
