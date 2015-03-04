# Copyright (c) 2015, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.


import stix
import stix.utils as utils
import stix.bindings.incident as incident_binding
from stix.common import (
    vocabs, Identity, Statement, StructuredText, VocabString,
    InformationSource, Confidence
)
from stix.common.related import (
    GenericRelationshipList, RelatedIndicator, RelatedThreatActor, RelatedTTP,
    RelatedObservable, RelatedIncident
)
from stix.data_marking import Marking

# relative
from .affected_asset import AffectedAsset
from .property_affected import PropertyAffected
from .time import Time
from .external_id import ExternalID
from .impact_assessment import ImpactAssessment
from .coa import COATaken, COATime
from .history import History


class Incident(stix.Entity):
    _binding = incident_binding
    _binding_class = _binding.IncidentType
    _namespace = "http://stix.mitre.org/Incident-1"
    _version = "1.1.1"
    _ALL_VERSIONS = ("1.0", "1.0.1", "1.1", "1.1.1")

    def __init__(self, id_=None, idref=None, timestamp=None, title=None, description=None, short_description=None):
        self.id_ = id_ or stix.utils.create_id("incident")
        self.idref = idref
        self.version = None # self._version
        self.description = description
        self.short_description = short_description
        self.title = title
        self.status = None
        self.time = None
        self.victims = None
        self.attributed_threat_actors = AttributedThreatActors()
        self.related_indicators = RelatedIndicators()
        self.related_observables = RelatedObservables()
        self.related_incidents = RelatedIncidents()
        self.affected_assets = None
        self.categories = None
        self.intended_effects = None
        self.leveraged_ttps = LeveragedTTPs()
        self.discovery_methods = None
        self.reporter = None
        self.responders = None
        self.coordinators = None
        self.external_ids = None
        self.impact_assessment = None
        self.information_source = None
        self.security_compromise = None
        self.confidence = None
        self.coa_taken = None
        self.handling = None
        self.history = History()
    
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = utils.dates.now() if not idref else None
    
    @property
    def id_(self):
        return self._id
    
    @id_.setter
    def id_(self, value):
        if not value:
            self._id = None
        else:
            self._id = value
            self.idref = None
    
    @property
    def version(self):
        return self._version
    
    @version.setter
    def version(self, value):
        if not value:
            self._version = None
        else:
            utils.check_version(self._ALL_VERSIONS, value)
            self._version = value
    
    @property
    def idref(self):
        return self._idref
    
    @idref.setter
    def idref(self, value):
        if not value:
            self._idref = None
        else:
            self._idref = value
            self.id_ = None # unset id_ if idref is present
    
    @property
    def timestamp(self):
        return self._timestamp
    
    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = utils.dates.parse_value(value)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value:
            if isinstance(value, StructuredText):
                self._description = value
            else:
                self._description = StructuredText(value=value)
        else:
            self._description = None

    @property
    def short_description(self):
        return self._short_description

    @short_description.setter
    def short_description(self, value):
        if value:
            if isinstance(value, StructuredText):
                self._short_description = value
            else:
                self._short_description = StructuredText(value=value)
        else:
            self._short_description = None

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        if not value:
            self._status = None
        elif isinstance(value, VocabString):
            self._status = value
        else:
            self._status = vocabs.IncidentStatus(value=value)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        if value and not isinstance(value, Time):
            raise ValueError("value must be instance of stix.incident.time.Time")

        self._time = value

    @property
    def handling(self):
        return self._handling
    
    @handling.setter
    def handling(self, value):
        if not value:
            self._handling = None
        elif isinstance(value, Marking):
            self._handling = value
        else:
            raise ValueError('unable to set handling to type %s' % type(value))
    @property
    def intended_effects(self):
        return self._intended_effects

    @intended_effects.setter
    def intended_effects(self, value):
        self._intended_effects = _IntendedEffects(value)

    def add_intended_effect(self, value):
        self.intended_effects.append(value)

    @property
    def victims(self):
        return self._victims

    @victims.setter
    def victims(self, value):
        self._victims = _Victims(value)

    def add_victim(self, victim):
        self._victims.append(victim)

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, value):
        self._categories = IncidentCategories(value)

    def add_category(self, category):
        self.categories.append(category)

    @property
    def affected_assets(self):
        return self._affected_assets
    
    @affected_assets.setter
    def affected_assets(self, value):
        self._affected_assets = AffectedAssets(value)
    
    def add_affected_asset(self, v):
       self.affected_assets.append(v)

    @property
    def discovery_methods(self):
        return self._discovery_methods

    @discovery_methods.setter
    def discovery_methods(self, value):
        self._discovery_methods = DiscoveryMethods(value)

    def add_discovery_method(self, value):
        self.discovery_methods.append(value)

    @property
    def reporter(self):
        return self._reporter

    @reporter.setter
    def reporter(self, value):
        if not value:
            self._reporter = None
        elif isinstance(value, InformationSource):
            self._reporter = value
        else:
            raise ValueError('value must be instance of InformationSource')

    @property
    def responders(self):
        return self._responders

    @responders.setter
    def responders(self, value):
        self._responders = _InformationSources(value)

    def add_responder(self, value):
        self.responders.append(value)

    @property
    def coordinators(self):
        return self._coordinators

    @coordinators.setter
    def coordinators(self, value):
        self._coordinators = _InformationSources(value)

    def add_coordinator(self, value):
        self.coordinators.append(value)

    @property
    def external_ids(self):
        return self._external_ids

    @external_ids.setter
    def external_ids(self, value):
        self._external_ids = _ExternalIDs(value)

    def add_external_id(self, value):
        self.external_ids.append(value)

    @property
    def impact_assessment(self):
        return self._impact_assessment

    @impact_assessment.setter
    def impact_assessment(self, value):
        if not value:
            self._impact_assessment = None
        elif isinstance(value, ImpactAssessment):
            self._impact_assessment = value
        else:
            raise ValueError('value must be instance of ImpactAssessment')

    @property
    def information_source(self):
        return self._information_source

    @information_source.setter
    def information_source(self, value):
        if not value:
            self._information_source = None
        elif isinstance(value, InformationSource):
            self._information_source = value
        else:
            raise ValueError('value must be instance of InformationSource')

    @property
    def security_compromise(self):
        return self._security_compromise

    @security_compromise.setter
    def security_compromise(self, value):
        if not value:
            self._security_compromise = None
        elif isinstance(value, VocabString):
            self._security_compromise = value
        else:
            self._security_compromise = vocabs.SecurityCompromise(value=value)

    @property
    def confidence(self):
        return self._confidence
    
    @confidence.setter
    def confidence(self, value):
        if not value:
            self._confidence = None
        elif isinstance(value, Confidence):
            self._confidence = value
        else:
            self._confidence = Confidence(value)

    @property
    def coa_taken(self):
        return self._coa_taken
    
    @coa_taken.setter
    def coa_taken(self, value):
        self._coa_taken = _COAsTaken(value)

    def add_coa_taken(self, value):
        self.coa_taken.append(value)

    def to_obj(self, return_obj=None, ns_info=None):
        super(Incident, self).to_obj(return_obj=return_obj, ns_info=ns_info)

        if not return_obj:
            return_obj = self._binding_class()

        return_obj.id = self.id_
        return_obj.idref = self.idref
        return_obj.timestamp = utils.dates.serialize_value(self.timestamp)
        return_obj.version = self.version
        return_obj.Title = self.title

        if self.description:
            return_obj.Description = self.description.to_obj(ns_info=ns_info)
        if self.short_description:
            return_obj.Short_Description = self.short_description.to_obj(ns_info=ns_info)
        if self.time:
            return_obj.Time = self.time.to_obj(ns_info=ns_info)
        if self.victims:
            return_obj.Victim = self.victims.to_obj(ns_info=ns_info)
        if self.attributed_threat_actors:
            return_obj.Attributed_Threat_Actors = self.attributed_threat_actors.to_obj(ns_info=ns_info)
        if self.related_indicators:
            return_obj.Related_Indicators = self.related_indicators.to_obj(ns_info=ns_info)
        if self.related_observables:
            return_obj.Related_Observables = self.related_observables.to_obj(ns_info=ns_info)
        if self.related_incidents:
            return_obj.Related_Incidents = self.related_incidents.to_obj(ns_info=ns_info)
        if self.categories:
            return_obj.Categories = self.categories.to_obj(ns_info=ns_info)
        if self.intended_effects:
            return_obj.Intended_Effect = self.intended_effects.to_obj(ns_info=ns_info)
        if self.leveraged_ttps:
            return_obj.Leveraged_TTPs = self.leveraged_ttps.to_obj(ns_info=ns_info)
        if self.affected_assets:
            return_obj.Affected_Assets = self.affected_assets.to_obj(ns_info=ns_info)
        if self.discovery_methods:
            return_obj.Discovery_Method = self.discovery_methods.to_obj(ns_info=ns_info)
        if self.reporter:
            return_obj.Reporter = self.reporter.to_obj(ns_info=ns_info)
        if self.responders:
            return_obj.Responder = self.responders.to_obj(ns_info=ns_info)
        if self.coordinators:
            return_obj.Coordinator = self.coordinators.to_obj(ns_info=ns_info)
        if self.external_ids:
            return_obj.External_ID = self.external_ids.to_obj(ns_info=ns_info)
        if self.impact_assessment:
            return_obj.Impact_Assessment = self.impact_assessment.to_obj(ns_info=ns_info)
        if self.information_source:
            return_obj.Information_Source = self.information_source.to_obj(ns_info=ns_info)
        if self.security_compromise:
            return_obj.Security_Compromise = self.security_compromise.to_obj(ns_info=ns_info)
        if self.confidence:
            return_obj.Confidence = self.confidence.to_obj(ns_info=ns_info)
        if self.coa_taken:
            return_obj.COA_Taken = self.coa_taken.to_obj(ns_info=ns_info)
        if self.status:
            return_obj.Status = self.status.to_obj(ns_info=ns_info)
        if self.handling:
            return_obj.Handling = self.handling.to_obj(ns_info=ns_info)
        if self.history:
            return_obj.History = self.history.to_obj(ns_info=ns_info)

        return return_obj

    @classmethod
    def from_obj(cls, obj, return_obj=None):
        if not obj:
            return None
        if not return_obj:
            return_obj = cls()

        return_obj.id_ = obj.id
        return_obj.idref = obj.idref
        return_obj.timestamp = obj.timestamp
        
        if isinstance(obj, cls._binding_class):
            return_obj.version = obj.version
            return_obj.title = obj.Title
            return_obj.description = StructuredText.from_obj(obj.Description)
            return_obj.short_description = StructuredText.from_obj(obj.Short_Description)
            return_obj.time = Time.from_obj(obj.Time)
            return_obj.victims = _Victims.from_obj(obj.Victim)
            return_obj.categories = IncidentCategories.from_obj(obj.Categories)
            return_obj.intended_effects = _IntendedEffects.from_obj(obj.Intended_Effect)
            return_obj.affected_assets = AffectedAssets.from_obj(obj.Affected_Assets)
            return_obj.discovery_methods = DiscoveryMethods.from_obj(obj.Discovery_Method)
            return_obj.coa_taken = _COAsTaken.from_obj(obj.COA_Taken)
            return_obj.confidence = Confidence.from_obj(obj.Confidence)
            return_obj.attributed_threat_actors = AttributedThreatActors.from_obj(obj.Attributed_Threat_Actors)
            return_obj.related_indicators = RelatedIndicators.from_obj(obj.Related_Indicators)
            return_obj.related_observables = RelatedObservables.from_obj(obj.Related_Observables)
            return_obj.leveraged_ttps = LeveragedTTPs.from_obj(obj.Leveraged_TTPs)
            return_obj.related_incidents = RelatedIncidents.from_obj(obj.Related_Incidents)
            return_obj.status = VocabString.from_obj(obj.Status)
            return_obj.handling = Marking.from_obj(obj.Handling)
            return_obj.history = History.from_obj(obj.History)
            return_obj.responders = _InformationSources.from_obj(obj.Responder)
            return_obj.coordinators = _InformationSources.from_obj(obj.Coordinator)
            return_obj.external_ids = _ExternalIDs.from_obj(obj.External_ID)
            return_obj.reporter = InformationSource.from_obj(obj.Reporter)
            return_obj.impact_assessment = ImpactAssessment.from_obj(obj.Impact_Assessment)
            return_obj.information_source = InformationSource.from_obj(obj.Information_Source)
            return_obj.security_compromise = VocabString.from_obj(obj.Security_Compromise)
            
        return return_obj

    def to_dict(self):
        return super(Incident, self).to_dict()

    @classmethod
    def from_dict(cls, dict_repr, return_obj=None):
        if not dict_repr:
            return None
        if not return_obj:
            return_obj = cls()

        get = dict_repr.get

        return_obj.id_ = get('id')
        return_obj.idref = get('idref')
        return_obj.timestamp = get('timestamp')
        return_obj.version = get('version')
        return_obj.title = get('title')
        return_obj.description = StructuredText.from_dict(get('description'))
        return_obj.short_description = StructuredText.from_dict(get('short_description'))
        return_obj.time = Time.from_dict(get('time'))
        return_obj.victims = _Victims.from_dict(get('victims'))
        return_obj.categories = IncidentCategories.from_dict(get('categories'))
        return_obj.attributed_threat_actors = AttributedThreatActors.from_dict(get('attributed_threat_actors'))
        return_obj.related_indicators = RelatedIndicators.from_dict(get('related_indicators'))
        return_obj.related_observables = RelatedObservables.from_dict(get('related_observables'))
        return_obj.related_incidents = RelatedIncidents.from_dict(get('related_incidents'))
        return_obj.intended_effects = _IntendedEffects.from_list(get('intended_effects'))
        return_obj.leveraged_ttps = LeveragedTTPs.from_dict(get('leveraged_ttps'))
        return_obj.affected_assets = AffectedAssets.from_dict(get('affected_assets'))
        return_obj.discovery_methods = DiscoveryMethods.from_dict(get('discovery_methods'))
        return_obj.reporter = InformationSource.from_dict(get('reporter'))
        return_obj.responders = _InformationSources.from_dict(get('responders'))
        return_obj.coordinators = _InformationSources.from_dict(get('coordinators'))
        return_obj.external_ids = _ExternalIDs.from_dict(get('external_ids'))
        return_obj.impact_assessment = ImpactAssessment.from_dict(get('impact_assessment'))
        return_obj.information_source = InformationSource.from_dict(get('information_source'))
        return_obj.security_compromise = VocabString.from_dict(get('security_compromise'))
        return_obj.confidence = Confidence.from_dict(get('confidence'))
        return_obj.coa_taken = _COAsTaken.from_dict(get('coa_taken'))
        return_obj.status = VocabString.from_dict(get('status'))
        return_obj.handling = Marking.from_dict(get('handling'))
        return_obj.history = History.from_dict(get('history'))
        
        return return_obj


class AttributedThreatActors(GenericRelationshipList):
    _namespace = "http://stix.mitre.org/Incident-1"
    _binding = incident_binding
    _binding_class = incident_binding.AttributedThreatActorsType
    _binding_var = "Threat_Actor"
    _contained_type = RelatedThreatActor
    _inner_name = "threat_actors"


class RelatedIndicators(GenericRelationshipList):
    _namespace = "http://stix.mitre.org/Incident-1"
    _binding = incident_binding
    _binding_class = incident_binding.RelatedIndicatorsType
    _binding_var = "Related_Indicator"
    _contained_type = RelatedIndicator
    _inner_name = "indicators"


class RelatedObservables(GenericRelationshipList):
    _namespace = "http://stix.mitre.org/Incident-1"
    _binding = incident_binding
    _binding_class = incident_binding.RelatedObservablesType
    _binding_var = "Related_Observable"
    _contained_type = RelatedObservable
    _inner_name = "observables"


class LeveragedTTPs(GenericRelationshipList):
    _namespace = "http://stix.mitre.org/Incident-1"
    _binding = incident_binding
    _binding_class = incident_binding.LeveragedTTPsType
    _binding_var = "Leveraged_TTP"
    _contained_type = RelatedTTP
    _inner_name = "ttps"
    

class RelatedIncidents(GenericRelationshipList):
    _namespace = "http://stix.mitre.org/Incident-1"
    _binding = incident_binding
    _binding_class = incident_binding.RelatedIncidentsType
    _binding_var = "Related_Incident"
    _contained_type = RelatedIncident
    _inner_name = "incidents"


class DiscoveryMethods(stix.EntityList):
    _namespace = "http://stix.mitre.org/Incident-1"
    _contained_type = VocabString

    def _fix_value(self, value):
        return vocabs.DiscoveryMethod(value)


class IncidentCategories(stix.EntityList):
    _namespace = "http://stix.mitre.org/Incident-1"
    _contained_type = VocabString
    _binding_class = incident_binding.CategoriesType
    _binding_var = "Category"
    _inner_name = "categories"
    _dict_as_list = True

    def _fix_value(self, value):
        return vocabs.IncidentCategory(value)


class AffectedAssets(stix.EntityList):
    _namespace = "http://stix.mitre.org/Incident-1"
    _contained_type = AffectedAsset
    _binding_class = incident_binding.AffectedAssetsType
    _binding_var = "Affected_Asset"
    _inner_name = "affected_assets"
    _dict_as_list = True


# NOT ACTUAL STIX TYPES!
class _COAsTaken(stix.TypedList):
    _contained_type =  COATaken


class _ExternalIDs(stix.TypedList):
    _contained_type = ExternalID


class _InformationSources(stix.TypedList):
    _contained_type = InformationSource


class _Victims(stix.TypedList):
    _contained_type = Identity

    def _fix_value(self, value):
        return Identity(name=value)


class _IntendedEffects(stix.TypedList):
    _contained_type = Statement

    def _fix_value(self, value):
        return Statement(value=vocabs.IntendedEffect(value))
