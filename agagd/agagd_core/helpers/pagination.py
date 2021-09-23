from django.core.paginator import Paginator


def agagd_paginator_helper(
    request, query_list_object, max_rows_per_page=50, page_request_get_value="pg"
):
    paginator = Paginator(query_list_object, max_rows_per_page)

    page_number = request.GET.get(page_request_get_value, 1)

    try:
        query_list_object_with_page_information = paginator.page(page_number)
    except PageNotAnInteger:
        query_list_object_with_page_information = paginator.page(1)
    except EmptyPage:
        query_list_object_with_page_information = paginator.page(paginator.num_pages)

    return query_list_object_with_page_information
