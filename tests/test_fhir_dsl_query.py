from phc.easy.query.fhir_dsl_query import build_query


def test_add_patient_ids_with_no_where_clause():
    assert build_query({}, patient_ids=["a"]) == {
        "where": {
            "query": {
                "terms": {"subject.reference.keyword": ["Patient/a", "a"]}
            }
        }
    }


def test_add_patient_id_with_query_term():
    result = build_query(
        {
            "where": {
                "type": "elasticsearch",
                "query": {"term": {"test.field.keyword": "blah"}},
            }
        },
        patient_ids=["a", "b"],
    )

    assert result == {
        "where": {
            "type": "elasticsearch",
            "query": {
                "bool": {
                    "should": [
                        {"term": {"test.field.keyword": "blah"}},
                        {
                            "terms": {
                                "subject.reference.keyword": [
                                    "Patient/a",
                                    "Patient/b",
                                    "a",
                                    "b",
                                ]
                            }
                        },
                    ],
                    "minimum_should_match": 2,
                }
            },
        }
    }


def test_add_patient_id_with_bool_should_query():
    result = build_query(
        {
            "where": {
                "type": "elasticsearch",
                "query": {
                    "bool": {"should": [{"term": {"gender.keyword": "male"}}]}
                },
            }
        },
        patient_ids=["a"],
        patient_key="id",
    )

    assert result == {
        "where": {
            "type": "elasticsearch",
            "query": {
                "bool": {
                    "should": [
                        {
                            "bool": {
                                "should": [
                                    {"term": {"gender.keyword": "male"}}
                                ],
                            }
                        },
                        {"terms": {"id.keyword": ["Patient/a", "a"]}},
                    ],
                    "minimum_should_match": 2,
                }
            },
        }
    }


def test_add_single_patient_id_to_query():
    result = build_query({}, patient_id="a")

    assert result == {
        "where": {
            "query": {
                "terms": {"subject.reference.keyword": ["Patient/a", "a"]}
            }
        }
    }
