<template lang="html">
    <div class="container">
      <div class="row">
        <div class="col-md-3">
          <h3>Inspection: {{ inspection.number }}</h3>
        </div>

      </div>
          <div class="col-md-3">
            <CommsLogs :comms_url="comms_url" :logs_url="logs_url" :comms_add_url="comms_add_url" :disable_add_entry="false"/>

            <div class="row">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        Workflow
                    </div>
                    <div class="panel-body panel-collapse">
                        <div class="row">
                            <div class="col-sm-12">
                                <strong>Status</strong><br/>
                                {{ statusDisplay }}<br/>
                            </div>
                        </div>
                        <Assignment 
                        :key="assignmentKey" 
                        @update-assigned-to-id="updateAssignedToId" 
                        :user_is_assignee="inspection.user_is_assignee"
                        :allowed_group_ids="inspection.allowed_groups"
                        :user_in_group="inspection.user_in_group" 
                        :assigned_to_id="inspection.assigned_to_id" 
                        :assign_url="assign_url"/>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        Action
                    </div>
                    <div class="panel-body panel-collapse">

                        <!--div v-if="statusId ==='open' && this.call_email.can_user_action" class="row action-button">
                          <div class="col-sm-12">
                                <a ref="save" @click="save()" class="btn btn-primary btn-block">
                                  Save
                                </a>
                          </div>
                        </div-->

                        <div class="row action-button">
                          <div v-if="sendToManagerVisibility" class="col-sm-12">
                                <a ref="close" @click="addWorkflow('send_to_manager')" class="btn btn-primary btn-block">
                                  Send to Manager
                                </a>
                          </div>
                        </div>

                        <div class="row action-button">
                          <div v-if="endorseVisibility" class="col-sm-12">
                                <a ref="close" @click="addWorkflow('endorse')" class="btn btn-primary btn-block">
                                  Endorse
                                </a>
                          </div>
                        </div>

                        <div class="row action-button">
                          <div v-if="requestAmendmentVisibility" class="col-sm-12">
                                <a ref="close" @click="addWorkflow('request_amendment')" class="btn btn-primary btn-block">
                                  Request Amendment
                                </a>
                          </div>
                        </div>

                        <div class="row action-button">
                          <div v-if="offenceVisibility" class="col-sm-12">
                                <a @click="open_offence()" class="btn btn-primary btn-block">
                                  Offence
                                </a>
                          </div>
                        </div>

                        <div  class="row action-button">
                          <div v-if="sanctionOutcomeVisibility" class="col-sm-12">
                                <a @click="open_sanction_outcome()" class="btn btn-primary btn-block">
                                  Sanction Outcome
                                </a>
                          </div>
                        </div>

                        <!--div  class="row action-button">
                          <div v-if="!readonlyForm" class="col-sm-12">
                                <a ref="close" @click="addWorkflow('close')" class="btn btn-primary btn-block">
                                  Close
                                </a>
                          </div>
                        </div-->

                    </div>
                </div>
            </div>



          </div>

          <div class="col-md-9" id="main-column">
            <div class="row">

                <div class="container-fluid">
                    <ul class="nav nav-pills aho2">
                        <li class="nav-item active"><a data-toggle="tab" :href="'#'+iTab">Inspection</a></li>
                        <li class="nav-item"><a data-toggle="tab" :href="'#'+lTab" @click="mapTabClicked">Location</a></li>
                        <li class="nav-item"><a data-toggle="tab" :href="'#'+cTab">Checklist</a></li>
                        <li class="nav-item"><a data-toggle="tab" :href="'#'+oTab">Outcomes</a></li>
                        <li class="nav-item"><a data-toggle="tab" :href="'#'+rTab">Related Items</a></li>
                    </ul>
                    <div class="tab-content">
                        <div :id="iTab" class="tab-pane fade in active">

                          <FormSection :formCollapse="false" label="Inspection Details" Index="0">

                            <div class="form-group">
                              <div class="row">
                                <div class="col-sm-3">
                                  <label>Inspection type</label>
                                </div>
                                <div class="col-sm-6">
                                  <select :disabled="readonlyForm" class="form-control" v-model="inspection.inspection_type_id" @change="loadSchema">
                                    <option  v-for="option in inspectionTypes" :value="option.id" v-bind:key="option.id">
                                      {{ option.inspection_type }}
                                    </option>
                                  </select>
                                </div>
                              </div>
                            </div>
                            <div class="form-group">
                              <div class="row">
                                <div class="col-sm-3">
                                  <label>Title</label>
                                </div>
                                <div class="col-sm-9">
                                  <input :readonly="readonlyForm" class="form-control" v-model="inspection.title"/>
                                </div>
                              </div>
                            </div>
                            <div class="form-group">
                              <div class="row">
                                <div class="col-sm-3">
                                  <label>Details</label>
                                </div>
                                <div class="col-sm-9">
                                  <textarea :readonly="readonlyForm" class="form-control" v-model="inspection.details"/>
                                </div>
                              </div>
                            </div>

                            <div class="form-group"><div class="row">
                                <label class="col-sm-3">Planned for (Date)</label>
                                <div class="col-sm-3">
                                    <div class="input-group date" ref="plannedForDatePicker">
                                        <input :disabled="readonlyForm" type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="inspection.planned_for_date" />
                                        <span class="input-group-addon">
                                            <span class="glyphicon glyphicon-calendar"></span>
                                        </span>
                                    </div>
                                </div>

                                <label class="col-sm-3">Planned for (Time)</label>
                                <div class="col-sm-3">
                                    <div class="input-group date" id="plannedForTimePicker">
                                      <input :disabled="readonlyForm" type="text" class="form-control" placeholder="HH:MM" v-model="inspection.planned_for_time"/>
                                      <span class="input-group-addon">
                                          <span class="glyphicon glyphicon-calendar"></span>
                                      </span>
                                    </div>
                                </div>
                            </div></div>
                            <!--div class="col-sm-12 form-group"><div class="row">
                                <label class="col-sm-4">Party Inspected</label>
                                    <input :disabled="readonlyForm" class="col-sm-1" id="individual" type="radio" v-model="inspection.party_inspected" v-bind:value="`individual`">
                                    <label class="col-sm-1" for="individual">Person</label>
                                    <input :disabled="readonlyForm" class="col-sm-1" id="organisation" type="radio" v-model="inspection.party_inspected" v-bind:value="`organisation`">
                                    <label class="col-sm-1" for="organisation">Organisation</label>
                            </div></div-->

                            <div class="form-group"><div class="row">
                                <SearchPersonOrganisation
                                componentTitle="Party to be inspected"
                                :parentEntity="inspectedEntity"
                                :excludeStaff="true"
                                :isEditable="!readonlyForm"
                                classNames="form-control"
                                :initialSearchType="inspection.party_inspected"
                                @entity-selected="entitySelected"
                                showCreateUpdate
                                ref="search_person_organisation"
                                v-bind:key="updateSearchPersonOrganisationBindId"/>
                                <!--div class="col-sm-1">
                                    <input type="button" class="btn btn-primary" value="Add" @click.prevent="addOffenderClicked()" />
                                </div-->
                                <!--div class="col-sm-2">
                                    <input :disabled="readonlyForm" type="button" class="btn btn-primary" value="Create New Person" @click.prevent="createNewPersonClicked()" />
                                </div-->
                            </div></div>
                            <!--div class="col-sm-12 form-group"><div class="row">
                                <div class="col-sm-12" v-if="!readonlyForm">
                                  <CreateNewPerson :displayComponent="displayCreateNewPerson" @new-person-created="newPersonCreated"/>
                                </div>
                                <div class="col-sm-12" v-if="!readonlyForm">
                                  <CreateNewOrganisation/>
                                </div>
                            </div></div-->
                            <div class="form-group"><div class="row">
                              <label class="col-sm-4" for="inspection_inform">Inform party to be inspected</label>
                              <input :disabled="readonlyForm" type="checkbox" id="inspection_inform" v-model="inspection.inform_party_being_inspected">

                            </div></div>
                          </FormSection>
                          <FormSection :formCollapse="false" label="Inspection Team" Index="1">
                            <div class="form-group">
                              <div class="row">
                                <div class="col-sm-6">
                                  <select :disabled="readonlyForm" class="form-control" ref="inspectionteam" >
                                    <option  v-for="option in inspection.all_officers" :value="option.id" v-bind:key="option.id">
                                      {{ option.full_name }}
                                    </option>
                                  </select>
                                </div>
                                <div class="col-sm-2">
                                    <button :disabled="readonlyForm" @click.prevent="addTeamMember" class="btn btn-primary">Add Member</button>
                                </div>
                                <!--div class="col-sm-2">
                                    <button @click.prevent="makeTeamLead" class="btn btn-primary">Make Team Lead</button>
                                </div-->
                                <!--div class="col-sm-2">
                                    <button @click.prevent="clearInspectionTeam" class="btn btn-primary pull-right">Clear</button>
                                </div-->
                              </div>
                            </div>
                            <div class="col-sm-12 form-group"><div class="row">
                                <div v-if="inspection">
                                    <datatable ref="inspection_team_table" id="inspection-team-table" :dtOptions="dtOptionsInspectionTeam" :dtHeaders="dtHeadersInspectionTeam" />
                                </div>
                            </div></div>
                          </FormSection>


                        </div>

                        <div :id="lTab" class="tab-pane fade in">
                            <FormSection :formCollapse="false" label="Location">
                                    <MapLocation 
                                        v-if="inspection.location" 
                                        :key="lTab" 
                                        ref="mapLocationComponent" 
                                        :readonly="readonlyForm" 
                                        :marker_longitude="inspection.location.geometry.coordinates[0]" 
                                        :marker_latitude="inspection.location.geometry.coordinates[1]" 
                                        @location-updated="locationUpdated"
                                    />
                                    <div :id="idLocationFieldsAddress" v-if="inspection.location">
                                        <div class="col-sm-12 form-group"><div class="row">
                                            <label class="col-sm-4">Street</label>
                                            <input class="form-control" v-model="inspection.location.properties.street" readonly />
                                        </div></div>
                                        <div class="col-sm-12 form-group"><div class="row">
                                            <label class="col-sm-4">Town/Suburb</label>
                                            <input class="form-control" v-model="inspection.location.properties.town_suburb" readonly />
                                        </div></div>
                                        <div class="col-sm-12 form-group"><div class="row">
                                            <label class="col-sm-4">State</label>
                                            <input class="form-control" v-model="inspection.location.properties.state" readonly />
                                        </div></div>
                                        <div class="col-sm-12 form-group"><div class="row">
                                            <label class="col-sm-4">Postcode</label>
                                            <input class="form-control" v-model="inspection.location.properties.postcode" readonly />
                                        </div></div>
                                        <div class="col-sm-12 form-group"><div class="row">
                                            <label class="col-sm-4">Country</label>
                                            <input class="form-control" v-model="inspection.location.properties.country" readonly />
                                        </div></div>
                                    </div>

                                    <div :id="idLocationFieldsDetails" v-if="inspection.location">
                                        <div class="col-sm-12 form-group"><div class="row">
                                            <label class="col-sm-4">Details</label>
                                            <textarea class="form-control location_address_field" v-model="inspection.location.properties.details" />
                                        </div></div>
                                    </div>
                            </FormSection>
                        </div>

                        <div :id="cTab" class="tab-pane fade in">
                            <FormSection :formCollapse="false" label="Checklist">
                                <div class="col-sm-12 form-group"><div class="row">
                                        <div v-if="rendererVisibility" v-for="(item, index) in current_schema">
                                      <compliance-renderer-block
                                         :component="item"
                                         :readonlyForm="readonlyForm"
                                         v-bind:key="`compliance_renderer_block${index}`"
                                        />
                                    </div>
                                </div></div>
                            </FormSection>
                        </div>
                        <div :id="oTab" class="tab-pane fade in">
                            <FormSection :formCollapse="false" label="Inspection report">
                                <div class="form-group">
                                    <div class="row">
                                        <div class="col-sm-6">
                                            <label class="control-label pull-left"  for="Name">Inspection report</label>
                                        </div>
                                        <div class="col-sm-9" v-if="inspection.inspectionReportDocumentUrl">
                                            <filefield
                                            ref="inspection_report_file"
                                            name="inspection-report-file"
                                            :isRepeatable="false"
                                            :documentActionUrl="inspection.inspectionReportDocumentUrl"
                                            @update-parent="loadInspectionReport"
                                            :readonly="readonlyForm"/>
                                        </div>
                                    </div>
                                </div>
                            </FormSection>
                        </div>
                        <div :id="rTab" class="tab-pane fade in">
                            <FormSection :formCollapse="false" label="Related Items">
                                <div class="col-sm-12 form-group"><div class="row">
                                    <div class="col-sm-12" v-if="relatedItemsVisibility">
                                        <RelatedItems v-bind:key="relatedItemsBindId" :parent_update_related_items="setRelatedItems" :readonlyForm="!canUserAction"/>
                                    </div>
                                </div></div>
                            </FormSection>
                        </div>
                    </div>
                </div>


            </div>
          </div>

        <div v-if="inspection.can_user_action" class="navbar navbar-fixed-bottom" style="background-color: #f5f5f5 ">
            <div class="navbar-inner">
                <div class="container">
                    <p class="pull-right" style="margin-top:5px;">
                        <input type="button" @click.prevent="save('exit')" class="btn btn-primary" value="Save and Exit"/>
                        <input type="button" @click.prevent="save('noexit')" class="btn btn-primary" value="Save and Continue"/>
                    </p>
                </div>
            </div>
        </div>
        <!--div v-if="workflow_type">
          <InspectionWorkflow ref="add_workflow" :workflow_type="workflow_type" v-bind:key="workflowBindId" />
        </div-->
        <div v-if="offenceInitialised">
            <Offence
            ref="offence"
            :parent_update_function="loadInspection"
            :region_id="inspection.region_id"
            :district_id="inspection.district_id"
            :allocated_group_id="inspection.allocated_group_id"
            v-bind:key="offenceBindId" />
        </div>
        <div v-if="sanctionOutcomeInitialised">
            <SanctionOutcome ref="sanction_outcome" :parent_update_function="loadInspection"/>
        </div>
        <InspectionWorkflow ref="inspection_workflow" :workflow_type="workflow_type" v-bind:key="workflowBindId" />
    </div>
</template>
<script>
import Vue from "vue";
import FormSection from "@/components/forms/section_toggle.vue";
import SearchPersonOrganisation from "@/components/common/search_person_or_organisation.vue";
//import CreateNewPerson from "@common-components/create_new_person.vue";
//import CreateNewOrganisation from "@common-components/create_new_organisation.vue";
import Assignment from "../assignment.vue";
import CommsLogs from "@common-components/comms_logs.vue";
import datatable from '@vue-utils/datatable.vue'
import { api_endpoints, helpers, cache_helper } from "@/utils/hooks";
import utils from "@/components/external/utils";
import { mapState, mapGetters, mapActions, mapMutations } from "vuex";
import moment from 'moment';
//import 'bootstrap/dist/css/bootstrap.css';
//import 'eonasdan-bootstrap-datetimepicker';
import Offence from '../offence/offence_modal';
import SanctionOutcome from '../sanction_outcome/sanction_outcome_modal';
import filefield from '@/components/common/compliance_file.vue';
import InspectionWorkflow from './inspection_workflow.vue';
import RelatedItems from "@common-components/related_items.vue";
import MapLocation from "../../common/map_location";
require("select2/dist/css/select2.min.css");
require("select2-bootstrap-theme/dist/select2-bootstrap.min.css");
import hash from 'object-hash';


export default {
  name: "ViewInspection",
  data: function() {
    return {
        mapboxAccessToken: null,
      uuid: 0,
      objectHash: null,
      iTab: 'iTab'+this._uid,
      rTab: 'rTab'+this._uid,
      oTab: 'oTab'+this._uid,
      cTab: 'cTab'+this._uid,
      lTab: 'lTab'+this._uid,
      current_schema: [],
      //createInspectionBindId: '',
      workflowBindId: '',
      //offenceBindId: '',
      //inspectionTeam: null,
      idLocationFieldsAddress: this.guid + "LocationFieldsAddress",
      idLocationFieldsDetails: this.guid + "LocationFieldsDetails",
      dtHeadersInspectionTeam: [
          'Name',
          'Role',
          'Action',
      ],
      dtOptionsInspectionTeam: {
          columns: [
              {
                  data: 'full_name',
              },
              {
                  data: 'member_role',
              },
              {
                  data: 'Action',
                  mRender: function(data, type, row) {
                      let links = '';
                      console.log("row.Action")
                      console.log(row.Action)
                      if (!row.Action.readonlyForm) {
                          if (row.Action.action === 'Member') {
                              links = '<a href="#" class="make_team_lead" data-member-id="' + row.Action.id + '">Make Team Lead</a><br>'
                          }
                          if (row.Action.can_remove) {
                              links += '<a href="#" class="remove_button" data-member-id="' + row.Action.id + '">Remove</a>'
                          }
                          return links
                      } else {
                          return ''
                      }
                  }
              },
          ]
      },
      workflow_type: '',

      sectionLabel: "Details",
      sectionIndex: 1,
      pBody: "pBody" + this._uid,
      loading: [],
      inspectionTypes: [],
      teamMemberSelected: null,
      displayCreateNewPerson: false,
      newPersonBeingCreated: false,
      comms_url: helpers.add_endpoint_json(
        api_endpoints.inspection,
        this.$route.params.inspection_id + "/comms_log"
      ),
      comms_add_url: helpers.add_endpoint_json(
        api_endpoints.inspection,
        this.$route.params.inspection_id + "/add_comms_log"
      ),
      logs_url: helpers.add_endpoint_json(
        api_endpoints.inspection,
        this.$route.params.inspection_id + "/action_log"
      ),
      assign_url: helpers.add_endpoint_join(
        api_endpoints.inspection,
        this.$route.params.inspection_id + '/update_assigned_to_id/'
      ),
      assignmentKey: 0,
      sanctionOutcomeInitialised: false,
      offenceInitialised: false,
      hashAttributeWhitelist: [
          "allocated_group_id",
          "details",
          "district_id",
          "individual_inspected_id",
          "inform_party_being_inspected",
          "inspection_type_id",
          "location",
          "organisation_inspected_id",
          "party_inspected",
          "planned_for_date",
          "planned_for_time",
          "region_id",
          "title",
          ],
    };
  },
  components: {
    CommsLogs,
    FormSection,
    datatable,
    SearchPersonOrganisation,
    //CreateNewPerson,
    //CreateNewOrganisation,
    Offence,
    SanctionOutcome,
    filefield,
    InspectionWorkflow,
    RelatedItems,
    MapLocation,
    Assignment,
  },
  computed: {
    ...mapGetters('inspectionStore', {
      inspection: "inspection",
    }),
    ...mapGetters({
        renderer_form_data: 'renderer_form_data'
    }),
    updateSearchPersonOrganisationBindId: function() {
        if (this.inspectedEntity.data_type && this.inspectedEntity.id) {
            return this.inspectedEntity.data_type + '_' + this.inspectedEntity.id
        }
    },
    csrf_token: function() {
      return helpers.getCookie("csrftoken");
    },
    statusDisplay: function() {
        return this.inspection.status ? this.inspection.status.name : '';
    },
    statusId: function() {
        return this.inspection.status ? this.inspection.status.id : '';
    },
    readonlyForm: function() {
        let readonly = true
        if (this.inspection.status && this.inspection.status.id === 'await_endorsement') {
        } else if (this.inspection.id) {
            readonly = !this.inspection.can_user_action;
        } else {
        }
        console.log(readonly)
        return readonly
    },
    canUserAction: function() {
        return this.inspection.can_user_action;
    },
    inspectionReportExists: function() {
        return this.inspection.inspection_report.length > 0 ? true : false;
    },
    offenceExists: function() {
        for (let item of this.inspection.related_items) {
            if (item.model_name.toLowerCase() === 'offence') {
                return true
            }
        }
        // return false if no related item is an Offence
        return false
    },
    sendToManagerVisibility: function() {
        if (this.inspection.status && this.inspection.can_user_action && this.inspectionReportExists) {
            //if (this.inspection.status.id.includes('open', 'request_amendment')) {
            if (this.inspection.status.id === 'open') {
                return true;
            }
        } else {
            return false;
        }
    },
    endorseVisibility: function() {
        if (this.inspection.status && this.inspection.can_user_action) {
            return this.inspection.status.id === 'await_endorsement' ? true : false;
        } else {
            return false;
        }
    },
    requestAmendmentVisibility: function() {
        if (this.inspection.status && this.inspection.can_user_action) {
            return this.inspection.status.id === 'await_endorsement' ? true : false;
        } else {
            return false;
        }
    },
    offenceVisibility: function() {
        if (this.inspection.status && this.inspection.can_user_action) {
            return this.inspection.status.id === 'open' ? true : false;
        } else {
            return false;
        }
    },
    sanctionOutcomeVisibility: function() {
        if (this.inspection.status && this.offenceExists && this.inspection.can_user_action) {
            return this.inspection.status.id === 'open' ? true : false;
        } else {
            return false;
        }
    },
    relatedItemsBindId: function() {
        let timeNow = Date.now()
        if (this.inspection && this.inspection.id) {
            return 'inspection_' + this.inspection.id + '_' + this._uid;
        } else {
            return timeNow.toString();
        }
    },
    relatedItemsVisibility: function() {
        if (this.inspection && this.inspection.id) {
            return true;
        } else {
            return false;
        }
    },
    rendererVisibility: function() {
        console.log("rendererVisibility")
        if (this.inspection.id && this.current_schema && this.current_schema.length > 0) {
            return true;
        } else {
            return false
        }
    },
    inspectedEntity: function() {
        let entity = {}
        if (this.inspection.individual_inspected) {
            entity.id = this.inspection.individual_inspected.id;
            entity.data_type = 'individual';
        } else if (this.inspection.organisation_inspected) {
            entity.id = this.inspection.organisation_inspected.id;
            entity.data_type = 'organisation';
        }
        return entity;
    },
    offenceBindId: function() {
        let offence_bind_id = ''
        //let timeNow = Date.now()
        //this.uuid += 1
        offence_bind_id = 'offence' + parseInt(this.uuid);
        return offence_bind_id;
    },
    inspectionTeam: function() {
        return this.inspection.inspection_team;
    },
  },
  filters: {
    formatDate: function(data) {
      return data ? moment(data).format("DD/MM/YYYY HH:mm:ss") : "";
    }
  },
  watch: {
      inspectionTeam: {
          handler: function (){
              this.constructInspectionTeamTable();
          },
          deep: true
      },
  },
  methods: {
    ...mapActions('inspectionStore', {
      loadInspection: 'loadInspection',
      saveInspection: 'saveInspection',
      setInspection: 'setInspection',
      setPlannedForTime: 'setPlannedForTime',
      // modifyInspectionTeam: 'modifyInspectionTeam',
      setPartyInspected: 'setPartyInspected',
      setRelatedItems: 'setRelatedItems',
    }),
        mapTabClicked: function() {
            // Call this function to render the map correctly
            // In some case, leaflet map is not rendered correctly...   Just partialy shown...
            if(this.$refs.mapLocationComponent){
                this.$refs.mapLocationComponent.invalidateSize();
            }
        },
        locationUpdated: function(latlng){
           // console.log('locationUpdated');
           // console.log(latlng);
           // // Update coordinate
           // this.inspection.location.geometry.coordinates[1] = latlng.lat;
           // this.inspection.location.geometry.coordinates[0] = latlng.lng;
           // // Update Address/Details
           // this.reverseGeocoding(latlng);
            // Update coordinate
            this.inspection.location.geometry.coordinates[1] = latlng.lat;
            this.inspection.location.geometry.coordinates[0] = latlng.lng;
            // Update Address/Details
            this.reverseGeocoding(latlng);
        },
        reverseGeocoding: function(coordinates_4326) {
          var self = this;

          $.ajax({
            url:
              api_endpoints.geocoding_address_search + coordinates_4326.lng + "," + coordinates_4326.lat + ".json?" +
              $.param({
                access_token: self.mapboxAccessToken,
                limit: 1,
                types: "address"
              }),
            dataType: "json",
            success: function(data, status, xhr) {
              let address_found = false;
              if (data.features && data.features.length > 0) {
                for (var i = 0; i < data.features.length; i++) {
                  if (data.features[i].place_type.includes("address")) {
                    self.setAddressFields(data.features[i]);
                    address_found = true;
                  }
                }
              }
              if (address_found) {
                self.showHideAddressDetailsFields(true, false);
                self.setLocationDetailsFieldEmpty();
              } else {
                self.showHideAddressDetailsFields(false, true);
                self.setLocationAddressEmpty();
              }
            }
          });
        },
        setAddressFields(feature) {
            if (this.inspection.location){
                  let state_abbr_list = {
                    "New South Wales": "NSW",
                    Queensland: "QLD",
                    "South Australia": "SA",
                    Tasmania: "TAS",
                    Victoria: "VIC",
                    "Western Australia": "WA",
                    "Northern Territory": "NT",
                    "Australian Capital Territory": "ACT"
                  };
                  let address_arr = feature.place_name.split(",");

                  /* street */
                  this.inspection.location.properties.street = address_arr[0];

                  /*
                   * Split the string into suburb, state and postcode
                   */
                  let reg = /^([a-zA-Z0-9\s]*)\s(New South Wales|Queensland|South Australia|Tasmania|Victoria|Western Australia|Northern Territory|Australian Capital Territory){1}\s+(\d{4})$/gi;
                  let result = reg.exec(address_arr[1]);

                  /* suburb */
                  this.inspection.location.properties.town_suburb = result[1].trim();

                  /* state */
                  let state_abbr = state_abbr_list[result[2].trim()];
                  this.inspection.location.properties.state = state_abbr;

                  /* postcode */
                  this.inspection.location.properties.postcode = result[3].trim();

                  /* country */
                  this.inspection.location.properties.country = "Australia";
            }
        },
        showHideAddressDetailsFields: function(showAddressFields, showDetailsFields) {
          if (showAddressFields) {
            $("#" + this.idLocationFieldsAddress).fadeIn();
          } else {
            $("#" + this.idLocationFieldsAddress).fadeOut();
          }
          if (showDetailsFields) {
            $("#" + this.idLocationFieldsDetails).fadeIn();
          } else {
            $("#" + this.idLocationFieldsDetails).fadeOut();
          }
        },
        setLocationAddressEmpty() {
            if(this.inspection.location){
                this.inspection.location.properties.town_suburb = "";
                this.inspection.location.properties.street = "";
                this.inspection.location.properties.state = "";
                this.inspection.location.properties.postcode = "";
                this.inspection.location.properties.country = "";
            }
        },
        setLocationDetailsFieldEmpty() {
            if(this.inspection.location){
                this.inspection.location.properties.details = "";
            }
        },
    constructInspectionTeamTable: function() {
        //console.log('constructInspectionTeamTable');
        //console.log(this.inspection.inspection_team);
        this.$refs.inspection_team_table.vmDataTable.clear().draw();

        if(this.inspection.inspection_team){
          for(let i = 0; i< this.inspection.inspection_team.length; i++){
            //let already_exists = this.$refs.related_items_table.vmDataTable.columns(0).data()[0].includes(this.displayedEntity.related_items[i].id);

            let actionColumn = new Object();
            Object.assign(actionColumn, this.inspection.inspection_team[i]);
            //actionColumn.can_user_action = this.inspection.can_user_action;
            actionColumn.readonlyForm = this.readonlyForm;
            // Prevent removal of last team member (plus blank entry)
            if (this.inspection.inspection_team.length > 2) {
                actionColumn.can_remove = true;
            }

            //if (!already_exists) {
            if (this.inspection.inspection_team[i].id) {
            this.$refs.inspection_team_table.vmDataTable.row.add(
                {
                    // 'id': this.inspectionTeam[i].id,
                    'full_name': this.inspection.inspection_team[i].full_name,
                    'member_role': this.inspection.inspection_team[i].member_role,
                    'Action': actionColumn,
                }
            ).draw();
            }
          }
        }
    },
    modifyInspectionTeam: async function({user_id, action}) {
        let inspectionTeamUrl = helpers.add_endpoint_join(
            api_endpoints.inspection,
            this.inspection.id + '/modify_inspection_team/'
            );
        let payload = {
            'user_id': user_id,
            'action': action
        }

        let inspectionTeamResponse = await Vue.http.post(inspectionTeamUrl, payload);
        await this.setInspection(inspectionTeamResponse.body);
        this.$nextTick(() => {
            this.constructInspectionTeamTable()
        });
    },
    newPersonCreated: async function(obj) {
        console.log(obj);
        if(obj.person){
            await this.setPartyInspected({data_type: 'individual', id: obj.person.id});

        // Set fullname and DOB into the input box
        let full_name = [obj.person.first_name, obj.person.last_name].filter(Boolean).join(" ");
        let dob = obj.person.dob ? "DOB:" + obj.person.dob : "DOB: ---";
        let value = [full_name, dob].filter(Boolean).join(", ");
        this.$refs.search_person.setInput(value);
      } else if (obj.err) {
        console.log(err);
      } else {
        // Should not reach here
      }
    },
    loadInspectionReport: async function() {
        console.log("loadInspectionReport")
        await this.loadInspection({inspection_id: this.inspection.id});
    },

    loadSchema: function() {
        if (this.inspection.inspection_type_id) {
          this.$nextTick(async function() {
          let url = helpers.add_endpoint_json(
                        api_endpoints.inspection_types,
                        this.inspection.inspection_type_id + '/get_schema',
                        );
          let returned_schema = await cache_helper.getSetCache(
            'InspectionTypeSchema',
            this.inspection.id.toString(),
            url);
          if (returned_schema) {
            this.current_schema = returned_schema.schema;
          }

          });
        }
    },

    open_sanction_outcome(){

      this.sanctionOutcomeInitialised = true;
      this.$nextTick(() => {
          this.$refs.sanction_outcome.isModalOpen = true;
      });
    },
    open_offence(){
      this.uuid += 1;
      this.offenceInitialised = true;
      this.$nextTick(() => {
          this.$refs.offence.isModalOpen = true;
      });
    },
    createNewPersonClicked: function() {
      this.newPersonBeingCreated = true;
      this.displayCreateNewPerson = !this.displayCreateNewPerson;
    },
    addTeamMember: async function() {
        await this.modifyInspectionTeam({
            user_id: this.teamMemberSelected,
            action: 'add'
        });
    },
    removeTeamMember: async function(e) {
        let memberId = e.target.getAttribute("data-member-id");
        await this.modifyInspectionTeam({
            user_id: memberId,
            action: 'remove'
        });
    },
    makeTeamLead: async function(e) {
        let memberId = e.target.getAttribute("data-member-id");
        await this.modifyInspectionTeam({
            user_id: memberId,
            action: 'make_team_lead'
        });
    },
    entitySelected: async function(para) {
        console.log(para);
        await this.setPartyInspected(para);
    },
    updateWorkflowBindId: function() {
        //let workflowBindId = ''
        let timeNow = Date.now()
        if (this.workflow_type) {
            this.workflowBindId = this.workflow_type + '_' + timeNow.toString();
        } else {
            this.workflowBindId = timeNow.toString();
        }
    },
    addWorkflow(workflow_type) {
      this.workflow_type = workflow_type;
      this.updateWorkflowBindId();
      this.$nextTick(() => {
        this.$refs.inspection_workflow.isModalOpen = true;
      });
      // this.$refs.add_workflow.isModalOpen = true;
    },
    save: async function(returnToDash) {
      console.log(returnToDash)
      let savedInspection = null;
      let savedPerson = null;
      if (this.inspection.id) {
          if (this.$refs.search_person_organisation && this.$refs.search_person_organisation.entityIsPerson) {
              console.log("savePerson")
              savedPerson = await this.$refs.search_person_organisation.parentSave()
              // if person save ok, continue with Inspection save
              if (savedPerson && savedPerson.ok) {
                  savedInspection = await this.saveInspection({ create: false, internal: false });
              }
          } else {
              console.log("no savePerson")
              savedInspection = await this.saveInspection({ create: false, internal: false });
          }
      } else {
          savedInspection = await this.saveInspection({ create: true, internal: false });
      }
      this.calculateHash();
      //console.log(savedInspection);
      if (savedInspection && savedInspection.ok && returnToDash === 'exit') {
        // remove redundant eventListeners
        window.removeEventListener('beforeunload', this.leaving);
        window.removeEventListener('onblur', this.leaving);
        // return to dash
        this.$router.push({ name: 'internal-inspection-dash' });
      }
    },
    addEventListeners: function() {
      let vm = this;
      let el_fr_date = $(vm.$refs.plannedForDatePicker);
      let el_fr_time = $(vm.$refs.plannedForTimePicker);

      // "From" field
      el_fr_date.datetimepicker({
        format: "DD/MM/YYYY",
        minDate: "now",
        showClear: true
      });
      el_fr_date.on("dp.change", function(e) {
        if (el_fr_date.data("DateTimePicker").date()) {
          vm.inspection.planned_for_date = e.date.format("DD/MM/YYYY");
        } else if (el_fr_date.data("date") === "") {
          vm.inspection.planned_for_date = "";
        }
      });
      el_fr_time.datetimepicker({ format: "LT", showClear: true });
      el_fr_time.on("dp.change", function(e) {
        if (el_fr_time.data("DateTimePicker").date()) {
          vm.inspection.planned_for_time = e.date.format("LT");
        } else if (el_fr_time.data("date") === "") {
          vm.inspection.planned_for_time = "";
        }
      });
      $('#inspection-team-table').on(
          'click',
          '.remove_button',
          vm.removeTeamMember,
          );
      $('#inspection-team-table').on(
          'click',
          '.make_team_lead',
          vm.makeTeamLead,
          );
      window.addEventListener('beforeunload', this.leaving);
      window.addEventListener('onblur', this.leaving);
    },
    leaving: function(e) {
        let vm = this;
        let dialogText = '';
        if (this.formChanged()){
            e.returnValue = dialogText;
            return dialogText;
        }
    },
    formChanged: function(){
        let changed = false;
        let copiedInspection = {};
        Object.getOwnPropertyNames(this.inspection).forEach(
            (val, idx, array) => {
                if (this.hashAttributeWhitelist.includes(val)) {
                    copiedInspection[val] = this.inspection[val]
                }
            });
        this.addHashAttributes(copiedInspection);
        if(this.objectHash !== hash(copiedInspection)){
            changed = true;
        }
        return changed;
    },
    calculateHash: function() {
        let copiedInspection = {}
        Object.getOwnPropertyNames(this.inspection).forEach(
            (val, idx, array) => {
                if (this.hashAttributeWhitelist.includes(val)) {
                    copiedInspection[val] = this.inspection[val]
                }
            });
        this.addHashAttributes(copiedInspection);
        this.objectHash = hash(copiedInspection);
    },
    addHashAttributes: function(obj) {
        let copiedRendererFormData = Object.assign({}, this.renderer_form_data);
        obj.renderer_form_data = copiedRendererFormData;
        return obj;
    },
    updateAssignedToId: async function (body) {
        await this.setInspection(body);
        this.$nextTick(() => {
            this.constructInspectionTeamTable();
        });
        this.assignmentKey += 1;
    },
  },
  created: async function() {
      let temp_token = await this.retrieveMapboxAccessToken();
      this.mapboxAccessToken = temp_token.access_token;

      if (this.$route.params.inspection_id) {
          await this.loadInspection({ inspection_id: this.$route.params.inspection_id });
      }
      console.log(this)

      // inspection_types
      let returned_inspection_types = await cache_helper.getSetCacheList(
          'InspectionTypes',
          api_endpoints.inspection_types
          );
      Object.assign(this.inspectionTypes, returned_inspection_types);
      // blank entry allows user to clear selection
      this.inspectionTypes.splice(0, 0,
          {
            id: null,
            description: "",
          });
      // load current Inspection renderer schema
      this.$nextTick(async () => {
          if (this.inspection.inspection_type_id) {
              await this.loadSchema();
          }
      });
      // calling modifyInspectionTeam with null parameters returns the current list
      //this.modifyInspectionTeam({user_id: null, action: null});
      // create object hash
      //this.object_hash = hash(this.inspection);
      this.calculateHash();
  },
  destroyed: function() {
      window.removeEventListener('beforeunload', this.leaving);
      window.removeEventListener('onblur', this.leaving);
  },

  mounted: function() {
      let vm = this;

      // Time field controls
      $('#plannedForTimePicker').datetimepicker({
              format: 'LT'
          });
      $('#plannedForTimePicker').on('dp.change', function(e) {
          vm.setPlannedForTime(e.date.format('LT'));
      });

      // Initialise select2 for officer list
      $(vm.$refs.inspectionteam).select2({
          "theme": "bootstrap",
          allowClear: true,
          placeholder:"Select Team Member"
                  }).
      on("select2:select",function (e) {
                          let selected = $(e.currentTarget);
                          vm.teamMemberSelected = selected.val();
                      }).
      on("select2:unselect",function (e) {
                          let selected = $(e.currentTarget);
                          vm.teamMemberSelected = selected.val();
                      });

      this.$nextTick(async () => {
          this.addEventListeners();
          this.constructInspectionTeamTable();
      });
  },
};
</script>

<style lang="css">
.action-button {
    margin-top: 5px;
}
#main-column {
  padding-left: 2%;
  padding-right: 0;
  margin-bottom: 50px;
}
.awesomplete {
    width: 100% !important;
}
.nav>li>a:focus, .nav>li>a:hover {
  text-decoration: none;
  background-color: #eee;
}
.nav-item {
  background-color: hsla(0, 0%, 78%, .8) !important;
  margin-bottom: 2px;
}
</style>
