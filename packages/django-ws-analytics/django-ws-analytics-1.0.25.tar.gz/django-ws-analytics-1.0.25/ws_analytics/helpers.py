import uuid

from django.db.models import Count, ExpressionWrapper, F, DateField, Avg, DurationField, Min, Max, Q, FloatField, \
    Window, Subquery, IntegerField, Sum, Case, When, Value, CharField
from django.db.models.functions import TruncDay, ExtractWeekDay, ExtractHour, TruncWeek, DenseRank, Lag, Concat
from django.utils import timezone

from models import AnalyticsDevice, AnalyticsRequest, AnalyticsSession


end_date = timezone.now()
start_date_sessions = end_date - timezone.timedelta(days=90)
start_date_requests = end_date - timezone.timedelta(days=60)

base_sessions = AnalyticsSession.objects.filter(expire_date__gte=start_date_sessions)
base_requests = AnalyticsRequest.objects.filter(timestamp__gte=start_date_requests)
base_devices = AnalyticsDevice.objects.all()

today = timezone.now().date()
start_of_last_week = today - timezone.timedelta(days=today.weekday(), weeks=1)
start_of_current_week = today - timezone.timedelta(days=today.weekday())
start_of_last_month = (today.replace(day=1) - timezone.timedelta(days=1)).replace(day=1)
start_of_current_month = today.replace(day=1)
last_30d = today - timezone.timedelta(days=30)
last_7d = today - timezone.timedelta(days=7)
one_week_ago = today - timezone.timedelta(days=today.weekday())


def get_current_online_devices():

    count = base_devices.filter(expire_date__gt=timezone.now()).count()
    return count


def get_current_online_sessions():

    count = base_sessions.filter(expire_date__gte=timezone.now()).count()
    return count


def get_sessions_data():

    todays_count = base_sessions.filter(expire_date__date=today).count()

    daily_counts_last_week = (base_sessions.filter(expire_date__gte=start_of_last_week)
                              .annotate(date=TruncDay('expire_date'))
                              .values('date')
                              .annotate(count=Count('id')).order_by('date'))

    weekly_counts_last_month = (base_sessions.filter(expire_date__gte=start_of_last_month)
                                .annotate(week=TruncWeek('expire_date'))
                                .values('week')
                                .annotate(count=Count('id')).order_by('week'))

    current_week_count = base_sessions.filter(expire_date__gte=start_of_current_week).count()

    current_month_count = base_sessions.filter(expire_date__gte=start_of_current_month).count()

    return {
        'todays_count': todays_count,
        'daily_counts_last_week': list(daily_counts_last_week),
        'weekly_counts_last_month': list(weekly_counts_last_month),
        'current_week_count': current_week_count,
        'current_month_count': current_month_count,
    }


def get_requests_data():

    todays_count = base_requests.filter(timestamp__date=today).count()

    daily_counts_last_week = (base_requests.filter(timestamp__gte=start_of_last_week,
                                                   timestamp__lt=start_of_current_week)
                              .annotate(date=TruncDay('timestamp'))
                              .values('date')
                              .annotate(count=Count('id')).order_by('date'))

    weekly_counts_last_month = (base_requests.filter(timestamp__gte=start_of_last_month,
                                                     timestamp__lt=start_of_current_month)
                                .annotate(week=TruncWeek('timestamp'))
                                .values('week')
                                .annotate(count=Count('id')).order_by('week'))

    current_week_count = base_requests.filter(timestamp__gte=start_of_current_week).count()

    current_month_count = base_requests.filter(timestamp__gte=start_of_current_month).count()

    return {
        'todays_count': todays_count,
        'daily_counts_last_week': list(daily_counts_last_week),
        'weekly_counts_last_month': list(weekly_counts_last_month),
        'current_week_count': current_week_count,
        'current_month_count': current_month_count,
    }


def get_daily_new_users_last_month():

    new_users = (
        base_devices
        .annotate(
            creation_date=ExpressionWrapper(F('expire_date') - timezone.timedelta(days=365), output_field=DateField()))
        .filter(creation_date__gte=last_30d, creation_date__lte=timezone.now())
        .values('creation_date')
        .annotate(count=Count('id'))
        .order_by('creation_date')
    )
    return list(new_users)


def get_device_usage_based_on_requests():

    def aggregate_for_attribute_based_on_requests(attribute_path):

        # Prepare queries to fetch requests within the last month and last week
        requests_last_month = AnalyticsRequest.objects.filter(timestamp__gte=last_30d).prefetch_related(
            'session', 'session__device')
        requests_last_week = AnalyticsRequest.objects.filter(timestamp__gte=last_7d).prefetch_related(
            'session', 'session__device')

        # Aggregate data based on device attributes by linking requests to devices
        last_month_data = requests_last_month.values(attribute_path).annotate(total=Count(attribute_path)).order_by(
            attribute_path)
        last_week_data = requests_last_week.values(attribute_path).annotate(total=Count(attribute_path)).order_by(
            attribute_path)
        day_of_week_data = (requests_last_month.annotate(day_of_week=TruncDay('timestamp')).values('day_of_week',
                                                                                                   attribute_path).
                            annotate(total=Count(attribute_path)).order_by('day_of_week', attribute_path))

        return {
            'last_month': list(last_month_data),
            'last_week': list(last_week_data),
            'day_of_week': list(day_of_week_data),
        }

    # Adjust the attribute paths to match the relationship through the session to the device
    device_type_data = aggregate_for_attribute_based_on_requests('analyticssession__analyticsdevice__device_type')
    device_data = aggregate_for_attribute_based_on_requests('analyticssession__analyticsdevice__device')
    system_data = aggregate_for_attribute_based_on_requests('analyticssession__analyticsdevice__system')
    browser_data = aggregate_for_attribute_based_on_requests('analyticssession__analyticsdevice__browser')

    return {
        'device_type_data': device_type_data,
        'device_data': device_data,
        'system_data': system_data,
        'browser_data': browser_data,
    }


def get_sessions_per_weekday():

    sessions_last_month = base_sessions.filter(
        expire_date__gte=start_of_last_month,
    )

    sessions_annotated = sessions_last_month.annotate(
        weekday=ExtractWeekDay('expire_date'),
        day=TruncDay('expire_date')
    )

    totals_per_weekday = sessions_annotated.values('weekday').annotate(
        total=Count('id')
    ).order_by('weekday')

    # Prepare data for average calculation
    daily_counts = sessions_annotated.values('day', 'weekday').annotate(
        daily_total=Count('id')
    )

    # Calculate averages per weekday
    averages_per_weekday = {}
    for weekday in range(1, 8):  # 1=Sunday, 7=Saturday
        weekday_counts = [entry['daily_total'] for entry in daily_counts if entry['weekday'] == weekday]
        if weekday_counts:
            averages_per_weekday[weekday] = sum(weekday_counts) / len(weekday_counts)
        else:
            averages_per_weekday[weekday] = 0

    totals_per_weekday_dict = {entry['weekday']: entry['total'] for entry in totals_per_weekday}

    sessions_per_weekday = {
        'totals': totals_per_weekday_dict,
        'averages': averages_per_weekday,
    }

    return sessions_per_weekday


def get_sessions_per_hour():

    # Filter sessions from the last month and for today
    sessions_last_month = base_sessions.filter(expire_date__gte=start_of_last_month)
    sessions_today = sessions_last_month.filter(expire_date__date=today)

    totals_per_hour_last_month = sessions_last_month.annotate(hour=ExtractHour('expire_date')).values('hour').annotate(
        total=Count('id')).order_by('hour')
    totals_per_hour_today = sessions_today.annotate(hour=ExtractHour('expire_date')).values('hour').annotate(
        total=Count('id')).order_by('hour')

    # Calculate averages for the last month
    total_sessions_last_month = sessions_last_month.count()
    hours_count_last_month = len(totals_per_hour_last_month)
    averages_per_hour_last_month = {entry['hour']: entry['total'] / total_sessions_last_month * hours_count_last_month
                                    for entry in totals_per_hour_last_month}

    totals_today = {entry['hour']: entry['total'] for entry in totals_per_hour_today}

    return {
        'last_month': {
            'totals': {entry['hour']: entry['total'] for entry in totals_per_hour_last_month},
            'averages': averages_per_hour_last_month,
        },
        'today': totals_today,
    }


def calculate_average_requests_per_session():

    total_avg_requests = base_requests.values('session').annotate(
        request_count=Count('id')
    ).aggregate(average_requests=Avg('request_count'))['average_requests']

    todays_avg_requests = base_requests.filter(
        timestamp__date=today
    ).values('session').annotate(
        request_count=Count('id')
    ).aggregate(average_requests=Avg('request_count'))['average_requests']

    last_week_avg_requests = base_requests.filter(
        timestamp__date__gte=last_7d
    ).annotate(
        day=TruncDay('timestamp')
    ).values('day').annotate(
        average_daily_requests=Avg('request_count')
    ).order_by('day')

    last_month_avg_requests = base_requests.filter(
        timestamp__gte=start_of_last_month
    ).annotate(
        week=TruncWeek('timestamp')
    ).values('week').annotate(
        average_weekly_requests=Avg('request_count')
    ).order_by('week')

    return {
        'total_average_requests_per_session': total_avg_requests,
        'todays_average_requests_per_session': todays_avg_requests,
        'last_week_daily_average_requests_per_session': list(last_week_avg_requests),
        'last_month_weekly_average_requests_per_session': list(last_month_avg_requests),
    }


def get_avg_duration(queryset):

    return queryset.values('id').annotate(
        duration=ExpressionWrapper(
            Max('analyticsrequest__timestamp') - Min('analyticsrequest__timestamp'),
            output_field=DurationField()
        )
    ).aggregate(average_duration=Avg('duration'))['avg_duration']


def calculate_average_session_duration():

    # Today's sessions for average duration
    today_sessions = AnalyticsSession.objects.filter(
        analyticsrequest__timestamp__date=today
    )
    today_avg_duration = get_avg_duration(today_sessions)

    # Daily average durations for the last week
    last_week_daily_avg_duration = {}
    for single_day in range(7):
        day = one_week_ago + timezone.timedelta(days=single_day)
        daily_sessions = AnalyticsSession.objects.filter(
            analyticsrequest__timestamp__date=day
        )
        last_week_daily_avg_duration[day] = get_avg_duration(daily_sessions)

    # Weekly average durations for last month
    last_month_weekly_avg_duration = AnalyticsSession.objects.filter(
        analyticsrequest__timestamp__gte=start_of_last_month
    ).annotate(
        week=TruncWeek('analyticsrequest__timestamp')
    ).values('week').annotate(average_duration=get_avg_duration(AnalyticsSession.objects)).order_by('week')

    return {
        'today_avg_duration': today_avg_duration,
        'last_week_daily_avg_duration': last_week_daily_avg_duration,
        'last_month_weekly_avg_duration': list(last_month_weekly_avg_duration),
    }


def aggregate_session_data_total_avg():

    def device_attribute_aggregation(attribute):

        today_filter = {'analyticsrequest__timestamp__date': today}
        last_week_filter = {'analyticsrequest__timestamp__gte': last_7d}
        last_month_filter = {'analyticsrequest__timestamp__gte': last_30d}

        # Aggregate counts
        today_count = AnalyticsSession.objects.filter(**today_filter).values(attribute).annotate(total=Count('id'))
        last_week_count = AnalyticsSession.objects.filter(**last_week_filter).annotate(
            day=TruncDay('analyticsrequest__timestamp')).values('day', attribute).annotate(total=Count('id'))
        last_month_count = AnalyticsSession.objects.filter(**last_month_filter).annotate(
            week=TruncWeek('analyticsrequest__timestamp')).values('week', attribute).annotate(total=Count('id'))

        # Calculate average durations
        today_avg_duration = get_avg_duration(AnalyticsSession.objects.filter(**today_filter))
        last_week_avg_duration = get_avg_duration(AnalyticsSession.objects.filter(**last_week_filter))
        last_month_avg_duration = get_avg_duration(AnalyticsSession.objects.filter(**last_month_filter))

        return {
            'today_count': list(today_count),
            'last_7d_daily_count': list(last_week_count),
            'last_30d_daily_count': list(last_month_count),
            'today_avg_duration': today_avg_duration,
            'last_7d_avg_duration': last_week_avg_duration,
            'last_30d_avg_duration': last_month_avg_duration
        }

    attributes = ['analyticsdevice__device_type', 'analyticsdevice__device',
                  'analyticsdevice__browser', 'analyticsdevice__system']
    results = {}

    for attribute in attributes:
        results[attribute] = device_attribute_aggregation(attribute)

    return results


def calculate_bounce_rate():

    # Filter sessions and requests based on the considered time periods
    sessions_last_month = (AnalyticsSession.objects.filter(analyticsrequest__timestamp__gte=start_of_last_month)
                           .prefetch_related('analyticsrequest'))

    def get_bounce_rate(queryset):

        # Count total sessions and bounces (sessions with only one request)
        total_sessions = queryset.count()
        bounces = queryset.annotate(requests_count=Count('analyticsrequest')).filter(requests_count=1).count()
        return (bounces / total_sessions) * 100 if total_sessions else 0

    bounce_rate_today = get_bounce_rate(sessions_last_month.filter(analyticsrequest__timestamp__date=today))

    # Daily bounce rates for the last week
    daily_bounce_rates = {}
    for i in range(7):
        day = last_7d + timezone.timedelta(days=i)
        bounce_rate = get_bounce_rate(sessions_last_month.filter(analyticsrequest__timestamp__date=day))
        daily_bounce_rates[day] = bounce_rate

    # Weekly bounce rates for the last month
    weekly_bounce_rates = sessions_last_month.annotate(week=TruncWeek('analyticsrequest__timestamp'),
                                                       request_count=Count('analyticsrequest')
                                                       ).values('week').annotate(
        week_start=ExpressionWrapper(F('week'), output_field=DateField()),
        total_sessions=Count('id', distinct=True),
        bounces=Sum(Case(When(requests_count=1, then=1), default=0, output_field=IntegerField()))
    ).annotate(
        bounce_rate=ExpressionWrapper(F('bounces') / F('total_sessions') * 100, output_field=FloatField())
    ).values('week_start', 'bounce_rate').order_by('week_start')

    return {
        'bounce_rate_today': bounce_rate_today,
        'daily_bounce_rates': daily_bounce_rates,
        'weekly_bounce_rates': list(weekly_bounce_rates),
    }


def aggregate_request_data(attribute, aggregate_func=Count):

    # Filter requests based on the time period
    requests_last_month = base_requests.filter(timestamp__gte=start_of_last_month)

    # Today's data
    todays_data = requests_last_month.filter(timestamp__date=today).values(attribute).annotate(
        total=aggregate_func(attribute)).order_by('-total')

    # Last week's daily data
    last_week_daily_data = requests_last_month.filter(timestamp__date__gte=last_7d).annotate(
        day=TruncDay('timestamp')).values('day', attribute).annotate(total=aggregate_func(attribute)).order_by('day',
                                                                                                               '-total')

    # Last month's weekly data
    last_month_weekly_data = requests_last_month.annotate(
        week=TruncWeek('timestamp')).values('week', attribute).annotate(total=aggregate_func(attribute)).order_by(
        'week', '-total')

    return {
        'today': list(todays_data),
        'last_7d_daily': list(last_week_daily_data),
        'last_month_weekly': list(last_month_weekly_data),
    }


def analyze_request_data():

    most_visited_pages = aggregate_request_data('path')
    return_codes = aggregate_request_data('status_code')
    methods = aggregate_request_data('method')
    average_execution_time = aggregate_request_data('execution_time', aggregate_func=Avg)
    cities = aggregate_request_data('city')
    countries = aggregate_request_data('country')

    analytics_data = {
        'most_visited_pages': most_visited_pages,
        'return_codes': return_codes,
        'methods': methods,
        'average_execution_time': average_execution_time,
        'cities': cities,
        'countries': countries
    }

    return analytics_data


# # how many active users have sent an application, today, last week daily, last month weekly
# def get_unique_submissions_by_users():
#     last_month_queryset = AnalyticsRequest.objects.filter(timestamp__gte=start_of_last_month,
#                                                method="POST")
#
#     submission_requests_last_month = (last_month_queryset.values('session_device').annotate(week=TruncWeek('timestamp')).
#                                       values('week').annotate(count=Count('session__device'),
#                                                               distinct=True).order_by('week'))
#     submission_requests_last_day = (last_month_queryset.filter(timestamp__day=today).values('session_device').
#                                     annotate(count=Count('session__device'), distinct=True).order_by('count'))


def aggregate_error_data(attribute, time_period):
    """
    Aggregates error data based on the given attribute for requests with status codes above 400.
    - attribute: Field name to aggregate on (e.g., 'path', 'analyticsdevice__device', 'analyticsdevice__browser', 'analyticsdevice__system').
    - time_period: A tuple indicating the start and end dates for filtering the data.
    """
    start_date, end_date = time_period
    # Base queryset for requests with errors
    error_requests = AnalyticsRequest.objects.filter(
        timestamp__gte=start_date,
        timestamp__lte=end_date,
        status_code__gt=400
    )

    # If the attribute is related to the device, adjust the prefetch_related accordingly
    if 'analyticsdevice__' in attribute:
        error_requests = error_requests.prefetch_related('session__device')

    # Aggregate error data
    error_data = error_requests.values(attribute).annotate(
        total=Count(attribute)
    ).order_by('-total')

    return list(error_data)


def analyze_error_data_counts():

    attributes = ['path', 'analyticsdevice__device_type', 'analyticsdevice__browser', 'analyticsdevice__system']

    # Initialize a dictionary to hold the aggregated data
    aggregated_error_data = {}

    for attribute in attributes:
        aggregated_error_data[attribute] = {
            'today': aggregate_error_data(attribute, (today, today)),
            'last_7d': aggregate_error_data(attribute, (last_7d, today)),
            'last_month': aggregate_error_data(attribute, (last_30d, today)),
        }

    return aggregated_error_data


def aggregate_exit_pages():

    # Annotate each request with a rank based on timestamp, partitioned by session
    annotated_requests = base_requests.annotate(
        rank=Window(
            expression=DenseRank(),
            order_by=F('timestamp').desc(),
            partition_by=F('session')
        )
    ).filter(
        timestamp__gte=last_30d
    )

    last_requests = annotated_requests.filter(rank=1)

    def get_exit_pages_for_period(time_filter):

        filtered_requests = last_requests.filter(**time_filter)
        exit_pages = filtered_requests.values('path').annotate(total=Count('id')).order_by('-total')
        return list(exit_pages)

    exit_pages_today = get_exit_pages_for_period({'timestamp__date': today})
    exit_pages_last_week = get_exit_pages_for_period({'timestamp__gte': last_7d})
    exit_pages_last_month = get_exit_pages_for_period({'timestamp__gte': last_30d})

    return {
        'today': exit_pages_today,
        'last_7d': exit_pages_last_week,
        'last_30d': exit_pages_last_month,
    }


"""
https://help.analyticsedge.com/article/misunderstood-metrics-time-on-page-session-duration/
"""


def calculate_time_on_page():

    # Step 1: Annotate each request with the timestamp of the next request in the same session
    requests_with_next = base_requests.filter(timestamp__gte=start_of_last_month).annotate(
        next_timestamp=Window(
            expression=Lag('timestamp'),
            order_by=F('timestamp').asc(),
            partition_by='session'
        )
    )

    requests_with_time_on_page = requests_with_next.annotate(
        time_on_page=ExpressionWrapper(
            F('next_timestamp') - F('timestamp'),
            output_field=DurationField()
        )
    )

    def aggregate_time_on_page(start_date, end_date=None):

        filter_kwargs = {
            'timestamp__date__gte': start_date,
        }
        if end_date:
            filter_kwargs['timestamp__date__lte'] = end_date

        return requests_with_time_on_page.filter(**filter_kwargs).exclude(time_on_page__isnull=True).aggregate(
            avg_time_on_page=Avg('time_on_page')
        )['avg_time_on_page']

    today_avg_time = aggregate_time_on_page(today)
    last_week_avg_time = aggregate_time_on_page(one_week_ago, today)
    last_month_avg_time = aggregate_time_on_page(start_of_last_month, today)

    return {
        'today_avg_time_on_page': today_avg_time,
        'last_week_avg_time_on_page': last_week_avg_time,
        'last_month_avg_time_on_page': last_month_avg_time,
    }


"""
https://support.google.com/analytics/answer/6074676?hl=en#zippy=%2Cin-this-article
"""


def get_daily_retention_data(devices, sessions, days=7):

    retention_data = {}

    for days_offset in range(days):
        cohort_date = timezone.now().date() - timezone.timedelta(days=days_offset)
        cohort_devices = devices.filter(creation_date=cohort_date)

        daily_retention = {}

        for days_until_today in range(1, days_offset - 1):
            subsequent_date = cohort_date + timezone.timedelta(days=days_until_today)
            subsequent_sessions = sessions.filter(device__in=cohort_devices, expire_date__date=subsequent_date).values(
                'device'
            ).distinct()

            cohort_count = cohort_devices.count()
            if cohort_count > 0:
                retention_rate = (subsequent_sessions.count() / cohort_count) * 100
                daily_retention[subsequent_date] = retention_rate

        retention_data[cohort_date] = daily_retention

    return retention_data


def get_weekly_retention_data(devices, sessions):

    retention_data = {}

    cohort_week_starts = devices.values('cohort_week').distinct().order_by('cohort_week')
    number_of_cohorts = len(cohort_week_starts)

    for index, cohort_week in enumerate(cohort_week_starts):
        cohort_start = cohort_week['cohort_week']
        cohort_end = cohort_start + timezone.timedelta(days=6)
        cohort_devices = devices.filter(
            creation_date__gte=cohort_start,
            creation_date__lte=cohort_end
        )
        cohort_number = 1

        weekly_retention = {}

        for weeks_until_today in range(1, number_of_cohorts - index):
            subsequent_week_start = cohort_start + timezone.timedelta(weeks=weeks_until_today)
            subsequent_week_end = subsequent_week_start + timezone.timedelta(days=6)

            subsequent_sessions = sessions.filter(device__in=cohort_devices,
                                                  expire_date__gte=subsequent_week_start,
                                                  expire_date__lte=subsequent_week_end
                                                  ).values('device').distinct()

            cohort_count = cohort_devices.count()

            if cohort_count > 0:
                retention_rate = (subsequent_sessions.count() / cohort_count) * 100
                weekly_retention[subsequent_week_start] = retention_rate

        cohort_number += 1

        retention_data[cohort_start] = weekly_retention

    return retention_data


def get_retention_data():

    total_queryset_device = AnalyticsDevice.objects.filter(
        expire_date__gt=start_of_last_month + timezone.timedelta(days=365)
    ).annotate(
        creation_date=ExpressionWrapper(
            F('expire_date') - timezone.timedelta(days=365), output_field=DateField()
        ),
        cohort_week=TruncWeek('creation_date')
    )

    total_queryset_session = AnalyticsSession.objects.filter(
        device__in=Subquery(total_queryset_device.values('pk')),
        expire_date__gte=start_of_last_month
    ).annotate(session_date_day=TruncDay('expire_date'), session_date_week=TruncWeek('expire_date'))

    daily_queryset_device = total_queryset_device.filter(
        creation_date__gte=last_7d
    )

    daily_queryset_session = total_queryset_session.filter(
        expire_date__gte=last_7d
    )

    daily_retention_data = get_daily_retention_data(daily_queryset_device, daily_queryset_session)

    weekly_retention_data = get_weekly_retention_data(total_queryset_device, total_queryset_session)

    retention_rates = {
        'daily_retention_rate': daily_retention_data,
        'weekly_retention_rate': weekly_retention_data,
    }

    return retention_rates


def generate_sankey_data_for_period(requests):

    # Fetch request data for the period, ordered by session and timestamp.
    requests = requests.annotate(
        prev_path=Window(
            expression=Lag('path'),
            order_by=F('timestamp').asc(),
            partition_by='session'
        )
    ).order_by('session', '-timestamp')

    requests = requests.annotate(
        link=Case(
            When(prev_path__isnull=True,
                 then=Concat(Value('Entry Point'), Value(' - '), 'path', output_field=CharField())),
            default=Concat('prev_path', Value(' - '), 'path', output_field=CharField()),
            output_field=CharField()
        )
    )

    link_counts = requests.values('link').annotate(total=Count('link')).order_by('-total')

    starting_path_counts = {}
    nodes = set()
    links = []

    for link_count in link_counts:
        source, target = link_count['link'].split(' - ')

        if source == 'Entry Point':
            starting_path_counts[target] = link_count['total']

        nodes.add(source)
        nodes.add(target)
        links.append({'source': source, 'target': target, 'value': link_count['total']})

    nodes_list = [{'name': node} for node in nodes]
    sankey_data = {'nodes': nodes_list, 'links': links}

    final_data = {
        'starting_paths': starting_path_counts,
        'sankey_data': sankey_data
    }

    return final_data


def get_sankey_starting_path_data():

    requests_last_month = base_requests.filter(timestamp__gte=start_of_last_month)

    requests_today = requests_last_month.filter(timestamp__date=today)

    requests_last_week = requests_last_month.filter(timestamp__gte=today - timezone.timedelta(days=6))

    data_today = generate_sankey_data_for_period(requests_today)
    data_week = generate_sankey_data_for_period(requests_last_week)
    data_month = generate_sankey_data_for_period(requests_last_month)

    data = {
        'data_today': data_today,
        'data_week': data_week,
        'data_month': data_month
    }

    return data


def get_sankey_starting_path_data_per_user(device_id=None):
    if not device_id:
        device_id = uuid.uuid4()

    requests_last_month = base_requests.filter(timestamp__gte=start_of_last_month,
                                               session__device__fingerprint=device_id)

    requests_today = requests_last_month.filter(timestamp__date=today)

    requests_last_week = requests_last_month.filter(timestamp__gte=today - timezone.timedelta(days=6))


    data_today = generate_sankey_data_for_period(requests_today)
    data_week = generate_sankey_data_for_period(requests_last_week)
    data_month = generate_sankey_data_for_period(requests_last_month)

    data = {
        'data_today': data_today,
        'data_week': data_week,
        'data_month': data_month
    }

    return data
