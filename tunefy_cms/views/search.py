from math import ceil


def get_paginated_context(collection, page_number, page_size):

    total_elements = collection.count()

    if total_elements == 0:
        return {
            'results': None,
            'total_pages': 0,
            'prev_page': None,
            'current_page': None,
            'next_page': None,
            'first_index': None,
            'page_size': 0
        }

    try:
        page_number = int(page_number)
        if page_number < 1:
            page_number = 1
    except (ValueError, TypeError):
        page_number = 1

    try:
        page_size = int(page_size)
        if page_size < 1:
            page_size = 1
        elif page_size > total_elements:
            page_size = total_elements
    except (ValueError, TypeError):
        page_size = total_elements

    total_pages = ceil(total_elements / page_size)
    if page_number > total_pages:
        page_number = total_pages

    first_idx = page_size * (page_number - 1)
    return {
        'results': collection[first_idx : first_idx + page_size],
        'total_pages': total_pages,
        'prev_page': (page_number - 1) if page_number > 1 else None,
        'current_page': page_number,
        'next_page': (page_number + 1) if page_number < total_pages else None,
        'first_index': first_idx,
        'page_size': page_size
    }