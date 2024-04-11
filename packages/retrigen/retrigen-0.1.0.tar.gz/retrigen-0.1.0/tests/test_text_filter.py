from retrigen import filter_text_by_td


def test_filter_text_by_td():
    documents = ["This is a small document which should be filtered"]

    filtered_docs = filter_text_by_td(documents)

    assert len(filtered_docs) == 0
