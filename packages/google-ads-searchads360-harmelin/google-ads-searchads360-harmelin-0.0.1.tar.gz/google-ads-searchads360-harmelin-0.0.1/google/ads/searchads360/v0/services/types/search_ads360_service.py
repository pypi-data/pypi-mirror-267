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

from google.ads.searchads360.v0.common.types import metrics as gasc_metrics
from google.ads.searchads360.v0.common.types import segments as gasc_segments
from google.ads.searchads360.v0.common.types import value
from google.ads.searchads360.v0.enums.types import summary_row_setting as gase_summary_row_setting
from google.ads.searchads360.v0.resources.types import ad_group as gasr_ad_group
from google.ads.searchads360.v0.resources.types import ad_group_ad as gasr_ad_group_ad
from google.ads.searchads360.v0.resources.types import ad_group_ad_label as gasr_ad_group_ad_label
from google.ads.searchads360.v0.resources.types import ad_group_audience_view as gasr_ad_group_audience_view
from google.ads.searchads360.v0.resources.types import ad_group_bid_modifier as gasr_ad_group_bid_modifier
from google.ads.searchads360.v0.resources.types import ad_group_criterion as gasr_ad_group_criterion
from google.ads.searchads360.v0.resources.types import ad_group_criterion_label as gasr_ad_group_criterion_label
from google.ads.searchads360.v0.resources.types import ad_group_label as gasr_ad_group_label
from google.ads.searchads360.v0.resources.types import age_range_view as gasr_age_range_view
from google.ads.searchads360.v0.resources.types import bidding_strategy as gasr_bidding_strategy
from google.ads.searchads360.v0.resources.types import campaign as gasr_campaign
from google.ads.searchads360.v0.resources.types import campaign_audience_view as gasr_campaign_audience_view
from google.ads.searchads360.v0.resources.types import campaign_budget as gasr_campaign_budget
from google.ads.searchads360.v0.resources.types import campaign_criterion as gasr_campaign_criterion
from google.ads.searchads360.v0.resources.types import campaign_label as gasr_campaign_label
from google.ads.searchads360.v0.resources.types import conversion_action as gasr_conversion_action
from google.ads.searchads360.v0.resources.types import customer as gasr_customer
from google.ads.searchads360.v0.resources.types import customer_client as gasr_customer_client
from google.ads.searchads360.v0.resources.types import customer_manager_link as gasr_customer_manager_link
from google.ads.searchads360.v0.resources.types import dynamic_search_ads_search_term_view as gasr_dynamic_search_ads_search_term_view
from google.ads.searchads360.v0.resources.types import gender_view as gasr_gender_view
from google.ads.searchads360.v0.resources.types import keyword_view as gasr_keyword_view
from google.ads.searchads360.v0.resources.types import label as gasr_label
from google.ads.searchads360.v0.resources.types import location_view as gasr_location_view
from google.ads.searchads360.v0.resources.types import product_group_view as gasr_product_group_view
from google.ads.searchads360.v0.resources.types import user_list as gasr_user_list
from google.ads.searchads360.v0.resources.types import webpage_view as gasr_webpage_view
from google.protobuf import field_mask_pb2  # type: ignore


__protobuf__ = proto.module(
    package='google.ads.searchads360.v0.services',
    marshal='google.ads.searchads360.v0',
    manifest={
        'SearchSearchAds360Request',
        'SearchSearchAds360Response',
        'SearchSearchAds360StreamRequest',
        'SearchSearchAds360StreamResponse',
        'SearchAds360Row',
        'CustomColumnHeader',
    },
)


class SearchSearchAds360Request(proto.Message):
    r"""Request message for
    [SearchAds360Service.Search][google.ads.searchads360.v0.services.SearchAds360Service.Search].

    Attributes:
        customer_id (str):
            Required. The ID of the customer being
            queried.
        query (str):
            Required. The query string.
        page_token (str):
            Token of the page to retrieve. If not specified, the first
            page of results will be returned. Use the value obtained
            from ``next_page_token`` in the previous response in order
            to request the next page of results.
        page_size (int):
            Number of elements to retrieve in a single
            page. When too large a page is requested, the
            server may decide to further limit the number of
            returned resources.
        validate_only (bool):
            If true, the request is validated but not
            executed.
        return_total_results_count (bool):
            If true, the total number of results that
            match the query ignoring the LIMIT clause will
            be included in the response. Default is false.
        summary_row_setting (google.ads.searchads360.v0.enums.types.SummaryRowSettingEnum.SummaryRowSetting):
            Determines whether a summary row will be
            returned. By default, summary row is not
            returned. If requested, the summary row will be
            sent in a response by itself after all other
            query results are returned.
    """

    customer_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    query: str = proto.Field(
        proto.STRING,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=4,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    return_total_results_count: bool = proto.Field(
        proto.BOOL,
        number=7,
    )
    summary_row_setting: gase_summary_row_setting.SummaryRowSettingEnum.SummaryRowSetting = proto.Field(
        proto.ENUM,
        number=8,
        enum=gase_summary_row_setting.SummaryRowSettingEnum.SummaryRowSetting,
    )


class SearchSearchAds360Response(proto.Message):
    r"""Response message for
    [SearchAds360Service.Search][google.ads.searchads360.v0.services.SearchAds360Service.Search].

    Attributes:
        results (MutableSequence[google.ads.searchads360.v0.services.types.SearchAds360Row]):
            The list of rows that matched the query.
        next_page_token (str):
            Pagination token used to retrieve the next page of results.
            Pass the content of this string as the ``page_token``
            attribute of the next request. ``next_page_token`` is not
            returned for the last page.
        total_results_count (int):
            Total number of results that match the query
            ignoring the LIMIT clause.
        field_mask (google.protobuf.field_mask_pb2.FieldMask):
            FieldMask that represents what fields were
            requested by the user.
        summary_row (google.ads.searchads360.v0.services.types.SearchAds360Row):
            Summary row that contains summary of metrics
            in results. Summary of metrics means aggregation
            of metrics across all results, here aggregation
            could be sum, average, rate, etc.
        custom_column_headers (MutableSequence[google.ads.searchads360.v0.services.types.CustomColumnHeader]):
            The headers of the custom columns in the
            results.
    """

    @property
    def raw_page(self):
        return self

    results: MutableSequence['SearchAds360Row'] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message='SearchAds360Row',
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    total_results_count: int = proto.Field(
        proto.INT64,
        number=3,
    )
    field_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=5,
        message=field_mask_pb2.FieldMask,
    )
    summary_row: 'SearchAds360Row' = proto.Field(
        proto.MESSAGE,
        number=6,
        message='SearchAds360Row',
    )
    custom_column_headers: MutableSequence['CustomColumnHeader'] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message='CustomColumnHeader',
    )


class SearchSearchAds360StreamRequest(proto.Message):
    r"""Request message for
    [SearchAds360Service.SearchStream][google.ads.searchads360.v0.services.SearchAds360Service.SearchStream].

    Attributes:
        customer_id (str):
            Required. The ID of the customer being
            queried.
        query (str):
            Required. The query string.
        batch_size (int):
            The number of rows that are returned in each
            stream response batch. When too large batch is
            requested, the server may decide to further
            limit the number of returned rows.
        summary_row_setting (google.ads.searchads360.v0.enums.types.SummaryRowSettingEnum.SummaryRowSetting):
            Determines whether a summary row will be
            returned. By default, summary row is not
            returned. If requested, the summary row will be
            sent in a response by itself after all other
            query results are returned.
    """

    customer_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    query: str = proto.Field(
        proto.STRING,
        number=2,
    )
    batch_size: int = proto.Field(
        proto.INT32,
        number=4,
    )
    summary_row_setting: gase_summary_row_setting.SummaryRowSettingEnum.SummaryRowSetting = proto.Field(
        proto.ENUM,
        number=3,
        enum=gase_summary_row_setting.SummaryRowSettingEnum.SummaryRowSetting,
    )


class SearchSearchAds360StreamResponse(proto.Message):
    r"""Response message for
    [SearchAds360Service.SearchStream][google.ads.searchads360.v0.services.SearchAds360Service.SearchStream].

    Attributes:
        results (MutableSequence[google.ads.searchads360.v0.services.types.SearchAds360Row]):
            The list of rows that matched the query.
        field_mask (google.protobuf.field_mask_pb2.FieldMask):
            FieldMask that represents what fields were
            requested by the user.
        summary_row (google.ads.searchads360.v0.services.types.SearchAds360Row):
            Summary row that contains summary of metrics
            in results. Summary of metrics means aggregation
            of metrics across all results, here aggregation
            could be sum, average, rate, etc.
        custom_column_headers (MutableSequence[google.ads.searchads360.v0.services.types.CustomColumnHeader]):
            The headers of the custom columns in the
            results.
        request_id (str):
            The unique id of the request that is used for
            debugging purposes.
    """

    results: MutableSequence['SearchAds360Row'] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message='SearchAds360Row',
    )
    field_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    summary_row: 'SearchAds360Row' = proto.Field(
        proto.MESSAGE,
        number=3,
        message='SearchAds360Row',
    )
    custom_column_headers: MutableSequence['CustomColumnHeader'] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message='CustomColumnHeader',
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class SearchAds360Row(proto.Message):
    r"""A returned row from the query.
    Attributes:
        ad_group (google.ads.searchads360.v0.resources.types.AdGroup):
            The ad group referenced in the query.
        ad_group_ad (google.ads.searchads360.v0.resources.types.AdGroupAd):
            The ad referenced in the query.
        ad_group_ad_label (google.ads.searchads360.v0.resources.types.AdGroupAdLabel):
            The ad group ad label referenced in the
            query.
        ad_group_audience_view (google.ads.searchads360.v0.resources.types.AdGroupAudienceView):
            The ad group audience view referenced in the
            query.
        ad_group_bid_modifier (google.ads.searchads360.v0.resources.types.AdGroupBidModifier):
            The bid modifier referenced in the query.
        ad_group_criterion (google.ads.searchads360.v0.resources.types.AdGroupCriterion):
            The criterion referenced in the query.
        ad_group_criterion_label (google.ads.searchads360.v0.resources.types.AdGroupCriterionLabel):
            The ad group criterion label referenced in
            the query.
        ad_group_label (google.ads.searchads360.v0.resources.types.AdGroupLabel):
            The ad group label referenced in the query.
        age_range_view (google.ads.searchads360.v0.resources.types.AgeRangeView):
            The age range view referenced in the query.
        bidding_strategy (google.ads.searchads360.v0.resources.types.BiddingStrategy):
            The bidding strategy referenced in the query.
        campaign_budget (google.ads.searchads360.v0.resources.types.CampaignBudget):
            The campaign budget referenced in the query.
        campaign (google.ads.searchads360.v0.resources.types.Campaign):
            The campaign referenced in the query.
        campaign_audience_view (google.ads.searchads360.v0.resources.types.CampaignAudienceView):
            The campaign audience view referenced in the
            query.
        campaign_criterion (google.ads.searchads360.v0.resources.types.CampaignCriterion):
            The campaign criterion referenced in the
            query.
        campaign_label (google.ads.searchads360.v0.resources.types.CampaignLabel):
            The campaign label referenced in the query.
        conversion_action (google.ads.searchads360.v0.resources.types.ConversionAction):
            The conversion action referenced in the
            query.
        customer (google.ads.searchads360.v0.resources.types.Customer):
            The customer referenced in the query.
        customer_manager_link (google.ads.searchads360.v0.resources.types.CustomerManagerLink):
            The CustomerManagerLink referenced in the
            query.
        customer_client (google.ads.searchads360.v0.resources.types.CustomerClient):
            The CustomerClient referenced in the query.
        dynamic_search_ads_search_term_view (google.ads.searchads360.v0.resources.types.DynamicSearchAdsSearchTermView):
            The dynamic search ads search term view
            referenced in the query.
        gender_view (google.ads.searchads360.v0.resources.types.GenderView):
            The gender view referenced in the query.
        keyword_view (google.ads.searchads360.v0.resources.types.KeywordView):
            The keyword view referenced in the query.
        label (google.ads.searchads360.v0.resources.types.Label):
            The label referenced in the query.
        location_view (google.ads.searchads360.v0.resources.types.LocationView):
            The location view referenced in the query.
        product_group_view (google.ads.searchads360.v0.resources.types.ProductGroupView):
            The product group view referenced in the
            query.
        user_list (google.ads.searchads360.v0.resources.types.UserList):
            The user list referenced in the query.
        webpage_view (google.ads.searchads360.v0.resources.types.WebpageView):
            The webpage view referenced in the query.
        metrics (google.ads.searchads360.v0.common.types.Metrics):
            The metrics.
        segments (google.ads.searchads360.v0.common.types.Segments):
            The segments.
        custom_columns (MutableSequence[google.ads.searchads360.v0.common.types.Value]):
            The custom columns.
    """

    ad_group: gasr_ad_group.AdGroup = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gasr_ad_group.AdGroup,
    )
    ad_group_ad: gasr_ad_group_ad.AdGroupAd = proto.Field(
        proto.MESSAGE,
        number=16,
        message=gasr_ad_group_ad.AdGroupAd,
    )
    ad_group_ad_label: gasr_ad_group_ad_label.AdGroupAdLabel = proto.Field(
        proto.MESSAGE,
        number=120,
        message=gasr_ad_group_ad_label.AdGroupAdLabel,
    )
    ad_group_audience_view: gasr_ad_group_audience_view.AdGroupAudienceView = proto.Field(
        proto.MESSAGE,
        number=57,
        message=gasr_ad_group_audience_view.AdGroupAudienceView,
    )
    ad_group_bid_modifier: gasr_ad_group_bid_modifier.AdGroupBidModifier = proto.Field(
        proto.MESSAGE,
        number=24,
        message=gasr_ad_group_bid_modifier.AdGroupBidModifier,
    )
    ad_group_criterion: gasr_ad_group_criterion.AdGroupCriterion = proto.Field(
        proto.MESSAGE,
        number=17,
        message=gasr_ad_group_criterion.AdGroupCriterion,
    )
    ad_group_criterion_label: gasr_ad_group_criterion_label.AdGroupCriterionLabel = proto.Field(
        proto.MESSAGE,
        number=121,
        message=gasr_ad_group_criterion_label.AdGroupCriterionLabel,
    )
    ad_group_label: gasr_ad_group_label.AdGroupLabel = proto.Field(
        proto.MESSAGE,
        number=115,
        message=gasr_ad_group_label.AdGroupLabel,
    )
    age_range_view: gasr_age_range_view.AgeRangeView = proto.Field(
        proto.MESSAGE,
        number=48,
        message=gasr_age_range_view.AgeRangeView,
    )
    bidding_strategy: gasr_bidding_strategy.BiddingStrategy = proto.Field(
        proto.MESSAGE,
        number=18,
        message=gasr_bidding_strategy.BiddingStrategy,
    )
    campaign_budget: gasr_campaign_budget.CampaignBudget = proto.Field(
        proto.MESSAGE,
        number=19,
        message=gasr_campaign_budget.CampaignBudget,
    )
    campaign: gasr_campaign.Campaign = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gasr_campaign.Campaign,
    )
    campaign_audience_view: gasr_campaign_audience_view.CampaignAudienceView = proto.Field(
        proto.MESSAGE,
        number=69,
        message=gasr_campaign_audience_view.CampaignAudienceView,
    )
    campaign_criterion: gasr_campaign_criterion.CampaignCriterion = proto.Field(
        proto.MESSAGE,
        number=20,
        message=gasr_campaign_criterion.CampaignCriterion,
    )
    campaign_label: gasr_campaign_label.CampaignLabel = proto.Field(
        proto.MESSAGE,
        number=108,
        message=gasr_campaign_label.CampaignLabel,
    )
    conversion_action: gasr_conversion_action.ConversionAction = proto.Field(
        proto.MESSAGE,
        number=103,
        message=gasr_conversion_action.ConversionAction,
    )
    customer: gasr_customer.Customer = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gasr_customer.Customer,
    )
    customer_manager_link: gasr_customer_manager_link.CustomerManagerLink = proto.Field(
        proto.MESSAGE,
        number=61,
        message=gasr_customer_manager_link.CustomerManagerLink,
    )
    customer_client: gasr_customer_client.CustomerClient = proto.Field(
        proto.MESSAGE,
        number=70,
        message=gasr_customer_client.CustomerClient,
    )
    dynamic_search_ads_search_term_view: gasr_dynamic_search_ads_search_term_view.DynamicSearchAdsSearchTermView = proto.Field(
        proto.MESSAGE,
        number=106,
        message=gasr_dynamic_search_ads_search_term_view.DynamicSearchAdsSearchTermView,
    )
    gender_view: gasr_gender_view.GenderView = proto.Field(
        proto.MESSAGE,
        number=40,
        message=gasr_gender_view.GenderView,
    )
    keyword_view: gasr_keyword_view.KeywordView = proto.Field(
        proto.MESSAGE,
        number=21,
        message=gasr_keyword_view.KeywordView,
    )
    label: gasr_label.Label = proto.Field(
        proto.MESSAGE,
        number=52,
        message=gasr_label.Label,
    )
    location_view: gasr_location_view.LocationView = proto.Field(
        proto.MESSAGE,
        number=123,
        message=gasr_location_view.LocationView,
    )
    product_group_view: gasr_product_group_view.ProductGroupView = proto.Field(
        proto.MESSAGE,
        number=54,
        message=gasr_product_group_view.ProductGroupView,
    )
    user_list: gasr_user_list.UserList = proto.Field(
        proto.MESSAGE,
        number=38,
        message=gasr_user_list.UserList,
    )
    webpage_view: gasr_webpage_view.WebpageView = proto.Field(
        proto.MESSAGE,
        number=162,
        message=gasr_webpage_view.WebpageView,
    )
    metrics: gasc_metrics.Metrics = proto.Field(
        proto.MESSAGE,
        number=4,
        message=gasc_metrics.Metrics,
    )
    segments: gasc_segments.Segments = proto.Field(
        proto.MESSAGE,
        number=102,
        message=gasc_segments.Segments,
    )
    custom_columns: MutableSequence[value.Value] = proto.RepeatedField(
        proto.MESSAGE,
        number=156,
        message=value.Value,
    )


class CustomColumnHeader(proto.Message):
    r"""Message for custom column header.
    Attributes:
        id (int):
            The custom column ID.
        name (str):
            The user defined name of the custom column.
        references_metrics (bool):
            True when the custom column references
            metrics.
    """

    id: int = proto.Field(
        proto.INT64,
        number=1,
    )
    name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    references_metrics: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
