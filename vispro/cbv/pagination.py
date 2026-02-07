from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def advanced_paginate(request, queryset, page_size=10, page_range=2):
    
    page = request.GET.get('page', 1)
    page_size = int(request.GET.get('page_size', page_size))

    paginator = Paginator(queryset, page_size)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    current_page = page_obj.number
    total_pages = paginator.num_pages

    start_page = max(current_page - page_range, 1)
    end_page = min(current_page + page_range, total_pages)

    return {
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': paginator.num_pages > 1,
        'current_page': current_page,
        'total_pages': total_pages,
        'page_range': range(start_page, end_page + 1),
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
    }
