import uuid

from django.db.models import Count, ExpressionWrapper, F, DateField, Avg, DurationField, Min, Max, FloatField, \
    Window, Subquery, IntegerField, Sum, Case, When, Value, CharField, Q
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import TruncDay, ExtractWeekDay, ExtractHour, TruncWeek, DenseRank, Lag, Concat
from django.utils import timezone

from .models import AnalyticsDevice, AnalyticsRequest, AnalyticsSession


class Analytics:
    def __init__(self):
        end_date = timezone.now()
        start_date_sessions = end_date - timezone.timedelta(days=90)
        start_date_requests = end_date - timezone.timedelta(days=60)

        self.base_sessions = AnalyticsSession.objects.filter(expire_date__gte=start_date_sessions)
        self.base_requests = AnalyticsRequest.objects.filter(timestamp__gte=start_date_requests)
        self.base_devices = AnalyticsDevice.objects.all()

        self.today = timezone.now().date()
        self.start_of_last_week = self.today - timezone.timedelta(days=self.today.weekday(), weeks=1)
        self.start_of_current_week = self.today - timezone.timedelta(days=self.today.weekday())
        self.start_of_last_month = (self.today.replace(day=1) - timezone.timedelta(days=1)).replace(day=1)
        self.start_of_current_month = self.today.replace(day=1)
        self.last_30d = self.today - timezone.timedelta(days=30)
        self.last_7d = self.today - timezone.timedelta(days=7)
        self.one_week_ago = self.today - timezone.timedelta(days=self.today.weekday())

    def get_current_online_devices(self):

        base = self.base_devices.filter(expire_date__gt=timezone.now())

        count = base.count()

        by_device_type = base.values('device_type').annotate(count=Count('session_key')).order_by('-count')
        by_device = base.values('device').annotate(count=Count('session_key')).order_by('-count')
        by_browser = base.values('browser').annotate(count=Count('session_key')).order_by('-count')
        by_system = base.values('system').annotate(count=Count('session_key')).order_by('-count')

        counts = {
            'count': count,
            'by_device_type': by_device_type,
            'by_device': by_device,
            'by_browser': by_browser,
            'by_system': by_system,
        }
        return counts

    def get_current_online_sessions(self):

        count = self.base_sessions.filter(expire_date__gte=timezone.now()).count()

        counts = {
            'count': count
        }

        return counts

    def get_sessions_data(self):

        todays_count = self.base_sessions.filter(expire_date__date=self.today).count()

        daily_counts_last_week = (self.base_sessions.filter(expire_date__gte=self.start_of_last_week)
                                  .annotate(date=TruncDay('expire_date'))
                                  .values('date')
                                  .annotate(count=Count('session_key')).order_by('date'))

        weekly_counts_last_month = (self.base_sessions.filter(expire_date__gte=self.start_of_last_month)
                                    .annotate(week=TruncWeek('expire_date'))
                                    .values('week')
                                    .annotate(count=Count('session_key')).order_by('week'))

        current_week_count = self.base_sessions.filter(expire_date__gte=self.start_of_current_week).count()

        current_month_count = self.base_sessions.filter(expire_date__gte=self.start_of_current_month).count()

        return {
            'todays_count': todays_count,
            'daily_counts_last_week': list(daily_counts_last_week),
            'weekly_counts_last_month': list(weekly_counts_last_month),
            'current_week_count': current_week_count,
            'current_month_count': current_month_count,
        }

    def get_requests_data(self):

        todays_count = self.base_requests.filter(timestamp__date=self.today).count()

        daily_counts_last_week = (self.base_requests.filter(timestamp__gte=self.start_of_last_week)
                                  .annotate(date=TruncDay('timestamp'))
                                  .values('date')
                                  .annotate(count=Count('id')).order_by('date'))

        weekly_counts_last_month = (self.base_requests.filter(timestamp__gte=self.start_of_last_month,
                                                              timestamp__lt=self.start_of_current_month)
                                    .annotate(week=TruncWeek('timestamp'))
                                    .values('week')
                                    .annotate(count=Count('id')).order_by('week'))

        current_week_count = self.base_requests.filter(timestamp__gte=self.start_of_current_week).count()

        current_month_count = self.base_requests.filter(timestamp__gte=self.start_of_current_month).count()

        return {
            'todays_count': todays_count,
            'daily_counts_last_week': list(daily_counts_last_week),
            'weekly_counts_last_month': list(weekly_counts_last_month),
            'current_week_count': current_week_count,
            'current_month_count': current_month_count,
        }

    def get_daily_new_users_last_month(self):

        new_users = (
            self.base_devices
            .annotate(
                creation_date=ExpressionWrapper(F('expire_date') - timezone.timedelta(days=365),
                                                output_field=DateField()))
            .annotate(date=TruncDay('creation_date'))
            .filter(date__gte=self.last_30d, date__lte=timezone.now())
            .values('date')
            .annotate(count=Count('fingerprint'))
            .order_by('date')
        )
        return list(new_users)

    def get_device_usage_based_on_requests(self):

        def aggregate_for_attribute_based_on_requests(attribute_path):
            # Prepare queries to fetch requests within the last month and last week
            requests_last_month = AnalyticsRequest.objects.filter(timestamp__gte=self.last_30d).prefetch_related(
                'session', 'session__device')
            requests_last_week = AnalyticsRequest.objects.filter(timestamp__gte=self.last_7d).prefetch_related(
                'session', 'session__device')

            # Aggregate data based on device attributes by linking requests to devices
            last_month_data = requests_last_month.values(attribute_path).annotate(total=Count('id')).order_by(
                '-total')
            last_week_data = requests_last_week.values(attribute_path).annotate(total=Count('id')).order_by(
                '-total')
            day_of_week_data = (requests_last_month.annotate(day_of_week=TruncDay('timestamp')).values('day_of_week',
                                                                                                       attribute_path).
                                annotate(total=Count('id')).order_by('day_of_week', '-total'))

            return {
                'last_month': list(last_month_data),
                'last_week': list(last_week_data),
                'day_of_week': list(day_of_week_data),
            }

        # Adjust the attribute paths to match the relationship through the session to the device
        device_type_data = aggregate_for_attribute_based_on_requests('session__device__device_type')
        device_data = aggregate_for_attribute_based_on_requests('session__device__device')
        system_data = aggregate_for_attribute_based_on_requests('session__device__system')
        browser_data = aggregate_for_attribute_based_on_requests('session__device__browser')

        return {
            'device_type_data': device_type_data,
            'device_data': device_data,
            'system_data': system_data,
            'browser_data': browser_data,
        }

    def get_sessions_per_weekday(self):

        sessions_last_month = self.base_sessions.filter(
            expire_date__gte=self.start_of_last_month,
        )

        sessions_annotated = sessions_last_month.annotate(
            weekday=ExtractWeekDay('expire_date'),
            day=TruncDay('expire_date')
        )

        totals_per_weekday = sessions_annotated.values('weekday').annotate(
            total=Count('session_key')
        ).order_by('weekday')

        # Prepare data for average calculation
        daily_counts = sessions_annotated.values('day', 'weekday').annotate(
            daily_total=Count('session_key')
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

    def get_sessions_per_hour(self):

        # Filter sessions from the last month and for self.today
        sessions_last_month = self.base_sessions.filter(expire_date__gte=self.start_of_last_month)
        sessions_today = sessions_last_month.filter(expire_date__date=self.today)

        totals_per_hour_last_month = sessions_last_month.annotate(hour=ExtractHour('expire_date')).values(
            'hour').annotate(
            total=Count('session_key')).order_by('hour')
        totals_per_hour_today = sessions_today.annotate(hour=ExtractHour('expire_date')).values(
            'hour').annotate(
            total=Count('session_key')).order_by('hour')

        # Calculate averages for the last month
        total_sessions_last_month = sessions_last_month.count()
        hours_range = range(24)

        totals_last_month = {hour: 0 for hour in hours_range}
        averages_per_hour_last_month = {hour: 0 for hour in hours_range}

        for entry in totals_per_hour_last_month:
            hour = entry['hour']
            total = entry['total']
            totals_last_month[hour] = total
            if total_sessions_last_month > 0:
                averages_per_hour_last_month[hour] = total / total_sessions_last_month

        totals_today = {hour: 0 for hour in range(24)}
        totals_today.update({entry['hour']: entry['total'] for entry in totals_per_hour_today})

        return {
            'last_month': {
                'totals': {entry['hour']: entry['total'] for entry in totals_per_hour_last_month},
                'averages': averages_per_hour_last_month,
            },
            'today': totals_today,
        }

    def calculate_average_requests_per_session(self):

        total_avg_requests = self.base_requests.values('session').annotate(
            request_count=Count('pk')
        ).aggregate(average_requests=Avg('request_count'))['average_requests']

        todays_avg_requests = self.base_requests.filter(
            timestamp__date=self.today
        ).values('session').annotate(
            request_count=Count('pk')
        ).aggregate(average_requests=Avg('request_count'))['average_requests']

        last_week_avg_requests = self.base_requests.filter(
            timestamp__date__gte=self.last_7d
        ).annotate(
            day=TruncDay('timestamp')
        ).values('day').annotate(
            request_count=Count('pk'),
            session_count=Count('session', distinct=True)
        ).order_by('day')

        daily_averages = {entry['day']: (entry['request_count'] / entry['session_count']
                                         if entry['session_count'] > 0 else 0) for entry in last_week_avg_requests}

        last_month_avg_requests = self.base_requests.filter(
            timestamp__gte=self.start_of_last_month
        ).annotate(
            week=TruncWeek('timestamp')
        ).values('week').annotate(
            request_count=Count('pk'),
            session_count=Count('session', distinct=True)
        ).order_by('week')

        weekly_averages = {entry['week']: (entry['request_count'] / entry['session_count']
                                           if entry['session_count'] > 0 else 0) for entry in last_month_avg_requests}

        return {
            'total_average_requests_per_session': total_avg_requests,
            'todays_average_requests_per_session': todays_avg_requests,
            'last_week_daily_average_requests_per_session': daily_averages,
            'last_month_weekly_average_requests_per_session': weekly_averages,
        }

    def calculate_average_session_duration(self):

        # Define a common annotation for duration to reuse in queries
        duration_annotation = ExpressionWrapper(
            Max('analyticsrequest__timestamp') - Min('analyticsrequest__timestamp'),
            output_field=DurationField()
        )

        # Today's sessions for average duration
        today_sessions = AnalyticsSession.objects.filter(
            analyticsrequest__timestamp__date=self.today
        ).annotate(duration=duration_annotation).aggregate(average_duration=Avg('duration'))['average_duration']

        # Daily average durations for the last week
        last_week_daily_avg_duration = {}
        for single_day in range(7):
            day = self.one_week_ago + timezone.timedelta(days=single_day)
            daily_avg_duration = AnalyticsSession.objects.filter(
                analyticsrequest__timestamp__date=day
            ).annotate(duration=duration_annotation).aggregate(average_duration=Avg('duration'))['average_duration']
            last_week_daily_avg_duration[day] = daily_avg_duration

        total_weeks = (timezone.now().date() - self.start_of_last_month).days // 7 + 1
        last_month_data = {}

        # Weekly average durations for last month
        for i in range(total_weeks):
            week_start_date = self.start_of_last_month + timezone.timedelta(days=i * 7)
            week_end_date = week_start_date + timezone.timedelta(days=6)

            weekly_sessions = AnalyticsSession.objects.filter(
                analyticsrequest__timestamp__date__gte=week_start_date,
                analyticsrequest__timestamp__date__lte=week_end_date
            ).annotate(duration=duration_annotation)

            weekly_average = weekly_sessions.aggregate(average_duration=Avg('duration'))['average_duration']
            last_month_data[week_start_date] = weekly_average or 0

        return {
            'today_avg_duration': today_sessions,
            'last_week_daily_avg_duration': last_week_daily_avg_duration,
            'last_month_weekly_avg_duration': last_month_data,
        }

    def aggregate_session_data_total_avg(self):

        duration_annotation = ExpressionWrapper(
            Max('analyticsrequest__timestamp') - Min('analyticsrequest__timestamp'),
            output_field=DurationField()
        )

        def device_attribute_aggregation(attribute):
            today_filter = {'analyticsrequest__timestamp__date': self.today}
            last_week_filter = {'analyticsrequest__timestamp__gte': self.last_7d}
            last_month_filter = {'analyticsrequest__timestamp__gte': self.last_30d}

            # Aggregate counts
            today_count = AnalyticsSession.objects.filter(**today_filter).values(attribute).annotate(
                total=Count('session_key'))
            last_week_count = AnalyticsSession.objects.filter(**last_week_filter).annotate(
                day=TruncDay('analyticsrequest__timestamp')).values('day', attribute).annotate(
                total=Count('session_key'))
            last_month_count = AnalyticsSession.objects.filter(**last_month_filter).annotate(
                week=TruncWeek('analyticsrequest__timestamp')).values('week', attribute).annotate(
                total=Count('session_key'))

            # # Calculate average durations
            # today_avg_duration = AnalyticsSession.objects.filter(**today_filter).annotate(
            # duration=duration_annotation).values(attribute, duration).annotate(
            # average_duration=Avg('duration')).order_by('-average_duration')
            # last_week_avg_duration = AnalyticsSession.objects.filter(**last_week_filter).annotate(
            # duration=duration_annotation).values(attribute, duration).annotate(
            # average_duration=Avg('duration')).order_by('-average_duration')
            # last_month_avg_duration = AnalyticsSession.objects.filter(**last_month_filter).annotate(
            # duration=duration_annotation).values(attribute, duration).annotate(
            # average_duration=Avg('duration')).order_by('-average_duration')

            return {
                'today_count': list(today_count),
                'last_7d_daily_count': list(last_week_count),
                'last_30d_daily_count': list(last_month_count),
                # 'today_avg_duration': today_avg_duration,
                # 'last_7d_avg_duration': last_week_avg_duration,
                # 'last_30d_avg_duration': last_month_avg_duration
            }

        attributes = ['device__device_type', 'device__device',
                      'device__browser', 'device__system']
        results = {}

        for attribute in attributes:
            results[attribute] = device_attribute_aggregation(attribute)

        return results

    def calculate_bounce_rate(self):

        # Filter sessions and requests based on the considered time periods
        sessions_last_month = (
            AnalyticsSession.objects.filter(analyticsrequest__timestamp__gte=self.last_7d)
            .prefetch_related('analyticsrequest'))

        def get_bounce_rate(queryset):
            # Count total sessions and bounces (sessions with only one request)
            total_sessions = queryset.count()
            bounces = queryset.annotate(requests_count=Count('analyticsrequest')).filter(requests_count=1).count()
            return (bounces / total_sessions) * 100 if total_sessions else 0

        bounce_rate_today = get_bounce_rate(
            sessions_last_month.filter(analyticsrequest__timestamp__date=self.today))

        # Daily bounce rates for the last week
        daily_bounce_rates = {}
        for i in range(7):
            day = self.last_7d + timezone.timedelta(days=i)
            bounce_rate = get_bounce_rate(sessions_last_month.filter(analyticsrequest__timestamp__date=day))
            daily_bounce_rates[day] = bounce_rate

        # # Weekly bounce rates for the last month
        # weekly_bounce_rates = {}
        #
        # for i in range(6):
        #     week_start_date = self.start_of_last_month + timezone.timedelta(days=i * 7)
        #     week_end_date = week_start_date + timezone.timedelta(days=6)
        #
        #     weekly_sessions = sessions_last_month.filter(
        #         analyticsrequest__timestamp__gte=week_start_date,
        #         analyticsrequest__timestamp__lte=week_end_date
        #     )
        #     weekly_bounce_rate = get_bounce_rate(weekly_sessions)
        #     weekly_bounce_rates[week_start_date.strftime("%Y-%m-%d")] = weekly_bounce_rate

        return {
            'bounce_rate_today': bounce_rate_today,
            'daily_bounce_rates': daily_bounce_rates,
            # 'weekly_bounce_rates': list(weekly_bounce_rates),
        }

    def aggregate_request_data(self, attribute_input, aggregate_func=Count):

        # Filter requests based on the time period
        requests_last_month = self.base_requests.filter(timestamp__gte=self.start_of_last_month)

        if attribute_input in ['city', 'country_name']:
            # attribute = KeyTextTransform(attribute_input, 'location')
            attribute = f"{attribute_input}__key"
            requests_last_month = requests_last_month.annotate(**{
                attribute: KeyTextTransform(attribute_input, 'location')
            })
        else:
            attribute = attribute_input

        # self.today's data
        todays_data = requests_last_month.filter(timestamp__date=self.today).values(attribute).annotate(
            total=aggregate_func(attribute)).order_by('-total')[:100]

        # Last week's daily data
        last_week_daily_data = requests_last_month.filter(timestamp__date__gte=self.last_7d).annotate(
            day=TruncDay('timestamp')).values('day', attribute).annotate(total=aggregate_func(attribute)).order_by(
            'day',
            '-total')[:100]

        # Last month's weekly data
        last_month_weekly_data = requests_last_month.annotate(
            week=TruncWeek('timestamp')).values('week', attribute).annotate(total=aggregate_func(attribute)).order_by(
            'week', '-total')[:100]

        return {
            'today': list(todays_data),
            'last_7d_daily': list(last_week_daily_data),
            'last_month_weekly': list(last_month_weekly_data),
        }

    def analyze_request_data(self):

        most_visited_pages = self.aggregate_request_data('path')
        return_codes = self.aggregate_request_data('status_code')
        methods = self.aggregate_request_data('method')
        # average_execution_time = self.aggregate_request_data('execution_time', aggregate_func=Avg)
        cities = self.aggregate_request_data('city')
        countries = self.aggregate_request_data('country_name')

        analytics_data = {
            'most_visited_pages': most_visited_pages,
            'return_codes': return_codes,
            'methods': methods,
            # 'average_execution_time': average_execution_time,
            'cities': cities,
            'countries': countries
        }

        return analytics_data

    def get_device_activity_submission_summary(self):
        requests = AnalyticsRequest.objects.filter(timestamp__gte=self.start_of_last_month)

        # Annotate each request with day and week
        requests = requests.annotate(
            day=TruncDay('timestamp'),
            week=TruncWeek('timestamp')
        )

        # Aggregate daily data
        daily_data = requests.values('day').annotate(
            total_devices=Count('session__device', distinct=True),
            post_devices=Count('session__device', filter=Q(method='POST'), distinct=True)
        ).order_by('day')

        # Gathering data for today and the last 7 days
        recent_data = {d['day']: {'total_devices': d['total_devices'], 'post_devices': d['post_devices']}
                       for d in daily_data if d['day'] >= timezone.now() - timezone.timedelta(days=7)}

        today_data = recent_data.get(self.today, {'total_devices': 0, 'post_devices': 0})

        # Aggregate weekly data
        weekly_data = requests.values('week').annotate(
            total_devices=Count('session__device', distinct=True),
            post_devices=Count('session__device', filter=Q(method='POST'), distinct=True)
        ).order_by('week')

        # Transforming weekly data into a more accessible format
        weekly_summary = {w['week']: {'total_devices': w['total_devices'], 'post_devices': w['post_devices']}
                          for w in weekly_data}

        return {
            'today_summary': today_data,
            'daily_summary': recent_data,
            'weekly_summary': weekly_summary,
        }

    def aggregate_error_data(self, attribute, time_period):
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

    def analyze_error_data_counts(self):

        attributes = ['path', 'session__device__device_type', 'session__device__browser', 'session__device__system']

        # Initialize a dictionary to hold the aggregated data
        aggregated_error_data = {}

        for attribute in attributes:
            aggregated_error_data[attribute] = {
                'today': self.aggregate_error_data(attribute, (self.today, self.today)),
                'last_7d': self.aggregate_error_data(attribute, (self.last_7d, self.today)),
                'last_month': self.aggregate_error_data(attribute, (self.last_30d, self.today)),
            }

        return aggregated_error_data

    def aggregate_exit_pages(self):

        # Annotate each request with a rank based on timestamp, partitioned by session
        annotated_requests = self.base_requests.annotate(
            rank=Window(
                expression=DenseRank(),
                order_by=F('timestamp').desc(),
                partition_by=F('session')
            )
        ).filter(
            timestamp__gte=self.last_30d
        )

        last_requests = annotated_requests.filter(rank=1)

        def get_exit_pages_for_period(time_filter):
            filtered_requests = last_requests.filter(**time_filter)
            exit_pages = filtered_requests.values('path').annotate(total=Count('id')).order_by('-total')
            return list(exit_pages)

        exit_pages_today = get_exit_pages_for_period({'timestamp__date': self.today})
        exit_pages_last_week = get_exit_pages_for_period({'timestamp__gte': self.last_7d})
        exit_pages_last_month = get_exit_pages_for_period({'timestamp__gte': self.last_30d})

        return {
            'today': exit_pages_today,
            'last_7d': exit_pages_last_week,
            'last_30d': exit_pages_last_month,
        }

    """
    https://help.analyticsedge.com/article/misunderstood-metrics-time-on-page-session-duration/
    """

    def calculate_time_on_page(self):

        # Step 1: Annotate each request with the timestamp of the next request in the same session
        requests_with_next = self.base_requests.filter(timestamp__gte=self.start_of_last_month).annotate(
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

        self.today_avg_time = aggregate_time_on_page(self.today)
        last_week_avg_time = aggregate_time_on_page(self.one_week_ago, self.today)
        last_month_avg_time = aggregate_time_on_page(self.start_of_last_month, self.today)

        return {
            'today_avg_time_on_page': self.today_avg_time,
            'last_week_avg_time_on_page': last_week_avg_time,
            'last_month_avg_time_on_page': last_month_avg_time,
        }

    """
    https://support.google.com/analytics/answer/6074676?hl=en#zippy=%2Cin-this-article
    """

    def get_daily_retention_data(self, devices, sessions, days=7):

        retention_data = {}

        for days_offset in range(days):
            cohort_date = timezone.now().date() - timezone.timedelta(days=days_offset)
            cohort_devices = devices.filter(creation_date=cohort_date)

            daily_retention = {}

            for days_until_today in range(1, days_offset - 1):
                subsequent_date = cohort_date + timezone.timedelta(days=days_until_today)
                subsequent_sessions = sessions.filter(device__in=cohort_devices,
                                                      expire_date__date=subsequent_date).values(
                    'device'
                ).distinct()

                cohort_count = cohort_devices.count()
                if cohort_count > 0:
                    retention_rate = (subsequent_sessions.count() / cohort_count) * 100
                    daily_retention[subsequent_date] = retention_rate

            retention_data[cohort_date] = daily_retention

        return retention_data

    def get_weekly_retention_data(self, devices, sessions):

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

    def get_retention_data_new_devices(self):

        total_queryset_device = AnalyticsDevice.objects.filter(
            expire_date__gt=self.start_of_last_month + timezone.timedelta(days=365)
        ).annotate(
            creation_date=ExpressionWrapper(
                F('expire_date') - timezone.timedelta(days=365), output_field=DateField()
            ),
            cohort_week=TruncWeek('creation_date')
        )

        data = self.get_retention_data(total_queryset_device)

        return data

    def get_retention_data_all_active_devices(self):
        # Adjust this query to get the last session date for each device
        last_session_dates = AnalyticsSession.objects.filter(
            expire_date__gte=self.start_of_last_month
        ).values('device').annotate(
            last_session_date=Max('expire_date')
        ).order_by()

        # Map devices to their last active session date
        device_to_last_session = {d['device']: d['last_session_date'] for d in last_session_dates}

        # Use this mapping to annotate your device queryset
        total_queryset_device = AnalyticsDevice.objects.filter(
            pk__in=device_to_last_session.keys()
        ).annotate(
            creation_date=Case(
                *[When(pk=device_id, then=Value(session_date)) for device_id, session_date in
                  device_to_last_session.items()],
                output_field=DateField()
            ),
            cohort_week=TruncWeek('creation_date')
        )

        data = self.get_retention_data(total_queryset_device)

        return data

    def get_retention_data(self, total_queryset_device):
        total_queryset_session = AnalyticsSession.objects.filter(
            device__in=Subquery(total_queryset_device.values('pk')),
            expire_date__gte=self.start_of_last_month
        ).annotate(session_date_day=TruncDay('expire_date'), session_date_week=TruncWeek('expire_date'))

        daily_queryset_device = total_queryset_device.filter(
            creation_date__gte=self.last_7d
        )

        daily_queryset_session = total_queryset_session.filter(
            expire_date__gte=self.last_7d
        )

        daily_retention_data = self.get_daily_retention_data(daily_queryset_device, daily_queryset_session)
        weekly_retention_data = self.get_weekly_retention_data(total_queryset_device, total_queryset_session)

        retention_rates = {
            'daily_retention_rate': daily_retention_data,
            'weekly_retention_rate': weekly_retention_data,
        }

        return retention_rates

    def generate_sankey_data_for_period(self, requests):
        # Fetch request data for the period, correctly handling window functions.
        # Immediately use 'prev_path' to compute 'link' in Python.
        annotated_requests = requests.annotate(
            prev_path=Window(
                expression=Lag('path'),
                order_by=F('timestamp').asc(),
                partition_by='session'
            )
        ).values('session', 'path', 'prev_path', 'timestamp').order_by('session', 'timestamp')

        # Initialize data structures for Sankey diagram
        link_counts = {}
        nodes = set()

        # Process each request to compute links and count occurrences
        for req in annotated_requests:
            prev_path = req['prev_path'] if req['prev_path'] is not None else "Entry Point"
            current_path = req['path']
            link = f"{prev_path} - {current_path}"

            if link in link_counts:
                link_counts[link] += 1
            else:
                link_counts[link] = 1

            nodes.update([prev_path, current_path])

        # Prepare the list of links with their counts
        links = [{'source': link.split(' - ')[0], 'target': link.split(' - ')[1], 'value': count}
                 for link, count in link_counts.items()]

        # Nodes need to be a list of dictionaries for many visualization libraries
        nodes_list = [{'name': node} for node in sorted(nodes)]
        sankey_data = {'nodes': nodes_list, 'links': links}

        # Calculate starting path counts from links directly
        starting_path_counts = {link.split(' - ')[1]: count for link, count in link_counts.items() if
                                link.startswith("Entry Point")}

        final_data = {
            'starting_paths': starting_path_counts,
            'sankey_data': sankey_data
        }

        return final_data

    def get_sankey_starting_path_data(self):

        requests_last_month = self.base_requests.filter(timestamp__gte=self.start_of_last_month)

        requests_today = requests_last_month.filter(timestamp__date=self.today)

        requests_last_week = requests_last_month.filter(timestamp__gte=self.today - timezone.timedelta(days=6))

        data_today = self.generate_sankey_data_for_period(requests_today)
        data_week = self.generate_sankey_data_for_period(requests_last_week)
        data_month = self.generate_sankey_data_for_period(requests_last_month)

        data = {
            'data_today': data_today,
            'data_week': data_week,
            'data_month': data_month
        }

        return data

    def get_sankey_starting_path_data_per_user(self, device_id=None):
        if not device_id:
            device_id = uuid.uuid4()

        requests_last_month = self.base_requests.filter(timestamp__gte=self.start_of_last_month,
                                                        session__device__fingerprint=device_id)

        requests_today = requests_last_month.filter(timestamp__date=self.today)

        requests_last_week = requests_last_month.filter(timestamp__gte=self.today - timezone.timedelta(days=6))

        data_today = self.generate_sankey_data_for_period(requests_today)
        data_week = self.generate_sankey_data_for_period(requests_last_week)
        data_month = self.generate_sankey_data_for_period(requests_last_month)

        data = {
            'data_today': data_today,
            'data_week': data_week,
            'data_month': data_month
        }

        return data

    def get_traffic_counts(self, queryset):
        source_count = queryset.values('utm_source').annotate(count=Count('id')).order_by('-count')
        medium_count = queryset.values('utm_medium').annotate(count=Count('id')).order_by('-count')

        return {'score': list(source_count), 'medium': list(medium_count)}

    def get_traffic_data(self):
        requests_last_month = self.base_requests.filter(timestamp__gte=self.start_of_last_month).exclude(
            query_params={})

        traffic_sources_since_last_month = requests_last_month.annotate(
            utm_source=KeyTextTransform('utm_source', 'query_params'),
            utm_medium=KeyTextTransform('utm_medium', 'query_params')
        )

        traffic_sources_current_month = traffic_sources_since_last_month.filter(
            timestamp__gte=self.start_of_current_month)
        traffic_sources_current_week = traffic_sources_since_last_month.filter(
            timestamp__gte=self.start_of_current_week)
        traffic_sources_today = traffic_sources_current_week.filter(timestamp__date=self.today)

        traffic_today = self.get_traffic_counts(traffic_sources_today)
        traffic_week = self.get_traffic_counts(traffic_sources_current_week)
        traffic_month = self.get_traffic_counts(traffic_sources_current_month)
        traffic_since_last_month = self.get_traffic_counts(traffic_sources_since_last_month)

        data = {
            'traffic_today': traffic_today,
            'traffic_week': traffic_week,
            'traffic_month': traffic_month,
            'traffic_since_last_month': traffic_since_last_month
        }

        return data

    def get_full_report(self):
        report = {
            "current_online_devices": self.get_current_online_devices(),
            "current_online_sessions": self.get_current_online_sessions(),
            "session_data": self.get_sessions_data(),
            "request_data": self.get_requests_data(),
            "daily_new_users_last_month": self.get_daily_new_users_last_month(),
            "device_usage_based_on_requests": self.get_device_usage_based_on_requests(),
            "sessions_per_weekday": self.get_sessions_per_weekday(),
            "sessions_per_hour": self.get_sessions_per_hour(),
            "average_requests_per_session": self.calculate_average_requests_per_session(),
            "average_session_duration": self.calculate_average_session_duration(),
            "session_data_total_avg": self.aggregate_session_data_total_avg(),
            "bounce_rate": self.calculate_bounce_rate(),
            "request_analysis": self.analyze_request_data(),
            "error_data_counts": self.analyze_error_data_counts(),
            "exit_pages": self.aggregate_exit_pages(),
            "time_on_page": self.calculate_time_on_page(),
            "retention_new_devices": self.get_retention_data_new_devices(),
            "retention_all_active_devices": self.get_retention_data_all_active_devices(),
            "sankey_starting_path_data": self.get_sankey_starting_path_data(),
            "traffic_data": self.get_traffic_data(),
            "device_activity": self.get_device_activity_submission_summary()
        }
        return report
