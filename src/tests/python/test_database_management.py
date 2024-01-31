def test_init(database_management):
    """Test if database management is initialized correctly"""
    assert database_management is not None


def test_add_video(database_management, single_item):
    """Test if a video is added correctly to the database"""
    ids = database_management.add_videos(*single_item)
    assert ids is not None
    assert len(ids) == 1
    database_management.delete_videos(*ids)


def test_add_videos(database_management, multiple_items):
    """Test if videos are added correctly to the database"""
    ids = database_management.add_videos(*multiple_items)
    assert ids is not None
    assert len(ids) == 2
    database_management.delete_videos(*ids)


def test_get_video(database_management, single_item):
    """Test if a video is retrieved correctly from the database"""
    ids = database_management.add_videos(*single_item)
    result = database_management.get_videos()
    assert result is not None
    assert result[-1].items() == single_item[0].items()
    database_management.delete_videos(*ids)


def test_delete_video(database_management, single_item):
    """Test if a video is deleted correctly from the database"""
    ids = database_management.add_videos(*single_item)
    assert database_management.delete_videos(*ids) == 1


def test_delete_videos(database_management, multiple_items):
    """Test if videos are deleted correctly from the database"""
    ids = database_management.add_videos(*multiple_items)
    assert database_management.delete_videos(*ids) == 2
