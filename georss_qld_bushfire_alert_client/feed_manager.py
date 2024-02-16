"""Queensland Bushfire Alert feed manager."""
from georss_client.feed_manager import FeedManagerBase

from .feed import QldBushfireAlertFeed


class QldBushfireAlertFeedManager(FeedManagerBase):
    """Feed Manager for Qld Bushfire Alert feed."""

    def __init__(
        self,
        generate_callback,
        update_callback,
        remove_callback,
        coordinates,
        filter_radius=None,
        filter_categories=None,
    ):
        """Initialize the Qld Bushfire Alert Feed Manager."""
        feed = QldBushfireAlertFeed(
            coordinates,
            filter_radius=filter_radius,
            filter_categories=filter_categories,
        )
        super().__init__(feed, generate_callback, update_callback, remove_callback)
