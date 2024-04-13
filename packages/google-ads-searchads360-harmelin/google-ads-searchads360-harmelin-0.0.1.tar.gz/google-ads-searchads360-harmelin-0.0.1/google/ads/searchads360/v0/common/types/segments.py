# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore

from google.ads.searchads360.v0.common.types import criteria
from google.ads.searchads360.v0.enums.types import conversion_action_category as gase_conversion_action_category
from google.ads.searchads360.v0.enums.types import day_of_week as gase_day_of_week
from google.ads.searchads360.v0.enums.types import device as gase_device


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.common',
    marshal='google.ads.searchads360.v0',
    manifest={
        'Segments',
        'Keyword',
    },
)


class Segments(proto.Message):
    r"""Segment only fields.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        conversion_action (str):
            Resource name of the conversion action.

            This field is a member of `oneof`_ ``_conversion_action``.
        conversion_action_category (google.ads.searchads360.v0.enums.types.ConversionActionCategoryEnum.ConversionActionCategory):
            Conversion action category.
        conversion_action_name (str):
            Conversion action name.

            This field is a member of `oneof`_ ``_conversion_action_name``.
        date (str):
            Date to which metrics apply.
            yyyy-MM-dd format, for example, 2018-04-17.

            This field is a member of `oneof`_ ``_date``.
        day_of_week (google.ads.searchads360.v0.enums.types.DayOfWeekEnum.DayOfWeek):
            Day of the week, for example, MONDAY.
        device (google.ads.searchads360.v0.enums.types.DeviceEnum.Device):
            Device to which metrics apply.
        keyword (google.ads.searchads360.v0.common.types.Keyword):
            Keyword criterion.
        month (str):
            Month as represented by the date of the first
            day of a month. Formatted as yyyy-MM-dd.

            This field is a member of `oneof`_ ``_month``.
        quarter (str):
            Quarter as represented by the date of the
            first day of a quarter. Uses the calendar year
            for quarters, for example, the second quarter of
            2018 starts on 2018-04-01. Formatted as
            yyyy-MM-dd.

            This field is a member of `oneof`_ ``_quarter``.
        week (str):
            Week as defined as Monday through Sunday, and
            represented by the date of Monday. Formatted as
            yyyy-MM-dd.

            This field is a member of `oneof`_ ``_week``.
        year (int):
            Year, formatted as yyyy.

            This field is a member of `oneof`_ ``_year``.
    """

    conversion_action: str = proto.Field(
        proto.STRING,
        number=146,
        optional=True,
    )
    conversion_action_category: gase_conversion_action_category.ConversionActionCategoryEnum.ConversionActionCategory = proto.Field(
        proto.ENUM,
        number=53,
        enum=gase_conversion_action_category.ConversionActionCategoryEnum.ConversionActionCategory,
    )
    conversion_action_name: str = proto.Field(
        proto.STRING,
        number=114,
        optional=True,
    )
    date: str = proto.Field(
        proto.STRING,
        number=79,
        optional=True,
    )
    day_of_week: gase_day_of_week.DayOfWeekEnum.DayOfWeek = proto.Field(
        proto.ENUM,
        number=5,
        enum=gase_day_of_week.DayOfWeekEnum.DayOfWeek,
    )
    device: gase_device.DeviceEnum.Device = proto.Field(
        proto.ENUM,
        number=1,
        enum=gase_device.DeviceEnum.Device,
    )
    keyword: 'Keyword' = proto.Field(
        proto.MESSAGE,
        number=61,
        message='Keyword',
    )
    month: str = proto.Field(
        proto.STRING,
        number=90,
        optional=True,
    )
    quarter: str = proto.Field(
        proto.STRING,
        number=128,
        optional=True,
    )
    week: str = proto.Field(
        proto.STRING,
        number=130,
        optional=True,
    )
    year: int = proto.Field(
        proto.INT32,
        number=131,
        optional=True,
    )


class Keyword(proto.Message):
    r"""A Keyword criterion segment.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        ad_group_criterion (str):
            The AdGroupCriterion resource name.

            This field is a member of `oneof`_ ``_ad_group_criterion``.
        info (google.ads.searchads360.v0.common.types.KeywordInfo):
            Keyword info.
    """

    ad_group_criterion: str = proto.Field(
        proto.STRING,
        number=3,
        optional=True,
    )
    info: criteria.KeywordInfo = proto.Field(
        proto.MESSAGE,
        number=2,
        message=criteria.KeywordInfo,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
