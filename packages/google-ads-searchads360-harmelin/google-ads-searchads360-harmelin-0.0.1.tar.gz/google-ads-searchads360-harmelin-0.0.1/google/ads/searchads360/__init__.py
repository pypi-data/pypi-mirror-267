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
import importlib
import sys


if sys.version_info < (3, 7):
    raise ImportError('This module requires Python 3.7 or later.')


_lazy_type_to_package_map = {
    # Message types
    'AgeRangeInfo': 'google.ads.searchads360.v0.common.types.criteria',
    'CustomParameter': 'google.ads.searchads360.v0.common.types.custom_parameter',
    'DeviceInfo': 'google.ads.searchads360.v0.common.types.criteria',
    'EnhancedCpc': 'google.ads.searchads360.v0.common.types.bidding',
    'FrequencyCapEntry': 'google.ads.searchads360.v0.common.types.frequency_cap',
    'GenderInfo': 'google.ads.searchads360.v0.common.types.criteria',
    'Keyword': 'google.ads.searchads360.v0.common.types.segments',
    'KeywordInfo': 'google.ads.searchads360.v0.common.types.criteria',
    'LanguageInfo': 'google.ads.searchads360.v0.common.types.criteria',
    'ListingGroupInfo': 'google.ads.searchads360.v0.common.types.criteria',
    'LocationGroupInfo': 'google.ads.searchads360.v0.common.types.criteria',
    'LocationInfo': 'google.ads.searchads360.v0.common.types.criteria',
    'ManualCpa': 'google.ads.searchads360.v0.common.types.bidding',
    'ManualCpc': 'google.ads.searchads360.v0.common.types.bidding',
    'ManualCpm': 'google.ads.searchads360.v0.common.types.bidding',
    'MaximizeConversions': 'google.ads.searchads360.v0.common.types.bidding',
    'MaximizeConversionValue': 'google.ads.searchads360.v0.common.types.bidding',
    'Metrics': 'google.ads.searchads360.v0.common.types.metrics',
    'PercentCpc': 'google.ads.searchads360.v0.common.types.bidding',
    'RealTimeBiddingSetting': 'google.ads.searchads360.v0.common.types.real_time_bidding_setting',
    'SearchAds360ExpandedDynamicSearchAdInfo': 'google.ads.searchads360.v0.common.types.ad_type_infos',
    'SearchAds360ExpandedTextAdInfo': 'google.ads.searchads360.v0.common.types.ad_type_infos',
    'SearchAds360ProductAdInfo': 'google.ads.searchads360.v0.common.types.ad_type_infos',
    'SearchAds360ResponsiveSearchAdInfo': 'google.ads.searchads360.v0.common.types.ad_type_infos',
    'SearchAds360TextAdInfo': 'google.ads.searchads360.v0.common.types.ad_type_infos',
    'Segments': 'google.ads.searchads360.v0.common.types.segments',
    'TargetCpa': 'google.ads.searchads360.v0.common.types.bidding',
    'TargetCpm': 'google.ads.searchads360.v0.common.types.bidding',
    'TargetImpressionShare': 'google.ads.searchads360.v0.common.types.bidding',
    'TargetingSetting': 'google.ads.searchads360.v0.common.types.targeting_setting',
    'TargetOutrankShare': 'google.ads.searchads360.v0.common.types.bidding',
    'TargetRestriction': 'google.ads.searchads360.v0.common.types.targeting_setting',
    'TargetRoas': 'google.ads.searchads360.v0.common.types.bidding',
    'TargetSpend': 'google.ads.searchads360.v0.common.types.bidding',
    'TextLabel': 'google.ads.searchads360.v0.common.types.text_label',
    'UserListInfo': 'google.ads.searchads360.v0.common.types.criteria',
    'Value': 'google.ads.searchads360.v0.common.types.value',
    'WebpageConditionInfo': 'google.ads.searchads360.v0.common.types.criteria',
    'WebpageInfo': 'google.ads.searchads360.v0.common.types.criteria',
    'AccountStatusEnum': 'google.ads.searchads360.v0.enums.types.account_status',
    'AccountTypeEnum': 'google.ads.searchads360.v0.enums.types.account_type',
    'AdGroupAdEngineStatusEnum': 'google.ads.searchads360.v0.enums.types.ad_group_ad_engine_status',
    'AdGroupAdRotationModeEnum': 'google.ads.searchads360.v0.enums.types.ad_group_ad_rotation_mode',
    'AdGroupAdStatusEnum': 'google.ads.searchads360.v0.enums.types.ad_group_ad_status',
    'AdGroupCriterionEngineStatusEnum': 'google.ads.searchads360.v0.enums.types.ad_group_criterion_engine_status',
    'AdGroupCriterionStatusEnum': 'google.ads.searchads360.v0.enums.types.ad_group_criterion_status',
    'AdGroupEngineStatusEnum': 'google.ads.searchads360.v0.enums.types.ad_group_engine_status',
    'AdGroupStatusEnum': 'google.ads.searchads360.v0.enums.types.ad_group_status',
    'AdGroupTypeEnum': 'google.ads.searchads360.v0.enums.types.ad_group_type',
    'AdServingOptimizationStatusEnum': 'google.ads.searchads360.v0.enums.types.ad_serving_optimization_status',
    'AdTypeEnum': 'google.ads.searchads360.v0.enums.types.ad_type',
    'AdvertisingChannelSubTypeEnum': 'google.ads.searchads360.v0.enums.types.advertising_channel_sub_type',
    'AdvertisingChannelTypeEnum': 'google.ads.searchads360.v0.enums.types.advertising_channel_type',
    'AgeRangeTypeEnum': 'google.ads.searchads360.v0.enums.types.age_range_type',
    'AssetFieldTypeEnum': 'google.ads.searchads360.v0.enums.types.asset_field_type',
    'AttributionModelEnum': 'google.ads.searchads360.v0.enums.types.attribution_model',
    'BiddingStrategyStatusEnum': 'google.ads.searchads360.v0.enums.types.bidding_strategy_status',
    'BiddingStrategySystemStatusEnum': 'google.ads.searchads360.v0.enums.types.bidding_strategy_system_status',
    'BiddingStrategyTypeEnum': 'google.ads.searchads360.v0.enums.types.bidding_strategy_type',
    'BudgetDeliveryMethodEnum': 'google.ads.searchads360.v0.enums.types.budget_delivery_method',
    'BudgetPeriodEnum': 'google.ads.searchads360.v0.enums.types.budget_period',
    'CampaignCriterionStatusEnum': 'google.ads.searchads360.v0.enums.types.campaign_criterion_status',
    'CampaignServingStatusEnum': 'google.ads.searchads360.v0.enums.types.campaign_serving_status',
    'CampaignStatusEnum': 'google.ads.searchads360.v0.enums.types.campaign_status',
    'ConversionActionCategoryEnum': 'google.ads.searchads360.v0.enums.types.conversion_action_category',
    'ConversionActionStatusEnum': 'google.ads.searchads360.v0.enums.types.conversion_action_status',
    'ConversionActionTypeEnum': 'google.ads.searchads360.v0.enums.types.conversion_action_type',
    'ConversionTrackingStatusEnum': 'google.ads.searchads360.v0.enums.types.conversion_tracking_status_enum',
    'CriterionTypeEnum': 'google.ads.searchads360.v0.enums.types.criterion_type',
    'CustomColumnValueTypeEnum': 'google.ads.searchads360.v0.enums.types.custom_column_value_type',
    'CustomerStatusEnum': 'google.ads.searchads360.v0.enums.types.customer_status',
    'DataDrivenModelStatusEnum': 'google.ads.searchads360.v0.enums.types.data_driven_model_status',
    'DayOfWeekEnum': 'google.ads.searchads360.v0.enums.types.day_of_week',
    'DeviceEnum': 'google.ads.searchads360.v0.enums.types.device',
    'GenderTypeEnum': 'google.ads.searchads360.v0.enums.types.gender_type',
    'InteractionEventTypeEnum': 'google.ads.searchads360.v0.enums.types.interaction_event_type',
    'KeywordMatchTypeEnum': 'google.ads.searchads360.v0.enums.types.keyword_match_type',
    'LabelStatusEnum': 'google.ads.searchads360.v0.enums.types.label_status',
    'ListingGroupTypeEnum': 'google.ads.searchads360.v0.enums.types.listing_group_type',
    'LocationGroupRadiusUnitsEnum': 'google.ads.searchads360.v0.enums.types.location_group_radius_units',
    'ManagerLinkStatusEnum': 'google.ads.searchads360.v0.enums.types.manager_link_status',
    'NegativeGeoTargetTypeEnum': 'google.ads.searchads360.v0.enums.types.negative_geo_target_type',
    'OptimizationGoalTypeEnum': 'google.ads.searchads360.v0.enums.types.optimization_goal_type',
    'PositiveGeoTargetTypeEnum': 'google.ads.searchads360.v0.enums.types.positive_geo_target_type',
    'QualityScoreBucketEnum': 'google.ads.searchads360.v0.enums.types.quality_score_bucket',
    'SearchAds360FieldCategoryEnum': 'google.ads.searchads360.v0.enums.types.search_ads360_field_category',
    'SearchAds360FieldDataTypeEnum': 'google.ads.searchads360.v0.enums.types.search_ads360_field_data_type',
    'SummaryRowSettingEnum': 'google.ads.searchads360.v0.enums.types.summary_row_setting',
    'TargetImpressionShareLocationEnum': 'google.ads.searchads360.v0.enums.types.target_impression_share_location',
    'TargetingDimensionEnum': 'google.ads.searchads360.v0.enums.types.targeting_dimension',
    'UserListTypeEnum': 'google.ads.searchads360.v0.enums.types.user_list_type',
    'WebpageConditionOperandEnum': 'google.ads.searchads360.v0.enums.types.webpage_condition_operand',
    'WebpageConditionOperatorEnum': 'google.ads.searchads360.v0.enums.types.webpage_condition_operator',
    'Ad': 'google.ads.searchads360.v0.resources.types.ad',
    'AdGroup': 'google.ads.searchads360.v0.resources.types.ad_group',
    'AdGroupAd': 'google.ads.searchads360.v0.resources.types.ad_group_ad',
    'AdGroupAdLabel': 'google.ads.searchads360.v0.resources.types.ad_group_ad_label',
    'AdGroupAudienceView': 'google.ads.searchads360.v0.resources.types.ad_group_audience_view',
    'AdGroupBidModifier': 'google.ads.searchads360.v0.resources.types.ad_group_bid_modifier',
    'AdGroupCriterion': 'google.ads.searchads360.v0.resources.types.ad_group_criterion',
    'AdGroupCriterionLabel': 'google.ads.searchads360.v0.resources.types.ad_group_criterion_label',
    'AdGroupLabel': 'google.ads.searchads360.v0.resources.types.ad_group_label',
    'AgeRangeView': 'google.ads.searchads360.v0.resources.types.age_range_view',
    'BiddingStrategy': 'google.ads.searchads360.v0.resources.types.bidding_strategy',
    'Campaign': 'google.ads.searchads360.v0.resources.types.campaign',
    'CampaignAudienceView': 'google.ads.searchads360.v0.resources.types.campaign_audience_view',
    'CampaignBudget': 'google.ads.searchads360.v0.resources.types.campaign_budget',
    'CampaignCriterion': 'google.ads.searchads360.v0.resources.types.campaign_criterion',
    'CampaignLabel': 'google.ads.searchads360.v0.resources.types.campaign_label',
    'ConversionAction': 'google.ads.searchads360.v0.resources.types.conversion_action',
    'ConversionTrackingSetting': 'google.ads.searchads360.v0.resources.types.customer',
    'CustomColumn': 'google.ads.searchads360.v0.resources.types.custom_column',
    'Customer': 'google.ads.searchads360.v0.resources.types.customer',
    'CustomerClient': 'google.ads.searchads360.v0.resources.types.customer_client',
    'CustomerManagerLink': 'google.ads.searchads360.v0.resources.types.customer_manager_link',
    'DoubleClickCampaignManagerSetting': 'google.ads.searchads360.v0.resources.types.customer',
    'DynamicSearchAdsSearchTermView': 'google.ads.searchads360.v0.resources.types.dynamic_search_ads_search_term_view',
    'GenderView': 'google.ads.searchads360.v0.resources.types.gender_view',
    'KeywordView': 'google.ads.searchads360.v0.resources.types.keyword_view',
    'Label': 'google.ads.searchads360.v0.resources.types.label',
    'LocationView': 'google.ads.searchads360.v0.resources.types.location_view',
    'ProductGroupView': 'google.ads.searchads360.v0.resources.types.product_group_view',
    'SearchAds360Field': 'google.ads.searchads360.v0.resources.types.search_ads360_field',
    'UserList': 'google.ads.searchads360.v0.resources.types.user_list',
    'WebpageView': 'google.ads.searchads360.v0.resources.types.webpage_view',
    'CustomColumnHeader': 'google.ads.searchads360.v0.services.types.search_ads360_service',
    'GetCustomColumnRequest': 'google.ads.searchads360.v0.services.types.custom_column_service',
    'GetSearchAds360FieldRequest': 'google.ads.searchads360.v0.services.types.search_ads360_field_service',
    'ListCustomColumnsRequest': 'google.ads.searchads360.v0.services.types.custom_column_service',
    'ListCustomColumnsResponse': 'google.ads.searchads360.v0.services.types.custom_column_service',
    'SearchAds360Row': 'google.ads.searchads360.v0.services.types.search_ads360_service',
    'SearchSearchAds360FieldsRequest': 'google.ads.searchads360.v0.services.types.search_ads360_field_service',
    'SearchSearchAds360FieldsResponse': 'google.ads.searchads360.v0.services.types.search_ads360_field_service',
    'SearchSearchAds360Request': 'google.ads.searchads360.v0.services.types.search_ads360_service',
    'SearchSearchAds360Response': 'google.ads.searchads360.v0.services.types.search_ads360_service',
    'SearchSearchAds360StreamRequest': 'google.ads.searchads360.v0.services.types.search_ads360_service',
    'SearchSearchAds360StreamResponse': 'google.ads.searchads360.v0.services.types.search_ads360_service',
    # Enum types
    # Client classes and transports
    'CustomColumnServiceClient': 'google.ads.searchads360.v0.services.services.custom_column_service',
    'CustomColumnServiceTransport': 'google.ads.searchads360.v0.services.services.custom_column_service.transports',
    'CustomColumnServiceGrpcTransport': 'google.ads.searchads360.v0.services.services.custom_column_service.transports',
    'SearchAds360FieldServiceClient': 'google.ads.searchads360.v0.services.services.search_ads360_field_service',
    'SearchAds360FieldServiceTransport': 'google.ads.searchads360.v0.services.services.search_ads360_field_service.transports',
    'SearchAds360FieldServiceGrpcTransport': 'google.ads.searchads360.v0.services.services.search_ads360_field_service.transports',
    'SearchAds360ServiceClient': 'google.ads.searchads360.v0.services.services.search_ads360_service',
    'SearchAds360ServiceTransport': 'google.ads.searchads360.v0.services.services.search_ads360_service.transports',
    'SearchAds360ServiceGrpcTransport': 'google.ads.searchads360.v0.services.services.search_ads360_service.transports',
}


# Background on how this behaves: https://www.python.org/dev/peps/pep-0562/
def __getattr__(name):  # Requires Python >= 3.7
    if name == '__all__':
        all_names = globals()['__all__'] = sorted(_lazy_type_to_package_map)
        return all_names
    elif name in _lazy_type_to_package_map:
        module = importlib.import_module(f'{_lazy_type_to_package_map[name]}')
        klass = getattr(module, name)
        globals()[name] = klass
        return klass
    else:
        raise AttributeError(f'unknown type {name!r}.')


def __dir__():
    return globals().get('__all__') or __getattr__('__all__')
