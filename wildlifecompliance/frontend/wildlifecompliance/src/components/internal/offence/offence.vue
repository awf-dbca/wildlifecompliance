<template lang="html">
    <div class="container">
        <div class="row">
            <div class="col-md-3">
                <h3>Offence: {{ displayLodgementNumber }}</h3>
            </div>
        </div>
        <div>
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
                            :user_is_assignee="offence.user_is_assignee"
                            :allowed_group_ids="offence.allowed_groups"
                            :user_in_group="offence.user_in_group" 
                            :assigned_to_id="offence.assigned_to_id" 
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
                            <div v-if="visibilitySanctionOutcomeButton" class="row action-button">
                                <div class="col-sm-12">
                                    <a @click="openSanctionOutcome()" class="btn btn-primary btn-block">
                                        Sanction Outcome
                                    </a>
                                </div>
                            </div>

                            <div v-if="visibilityCloseButton" class="row action-button">
                                <div class="col-sm-12">
                                    <a @click="addWorkflow('close')" class="btn btn-primary btn-block">
                                        Close
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-9" id="main-column">
                <div class="row">
                    <div class="container-fluid">
                        <ul class="nav nav-pills aho2">
                            <li class="nav-item active"><a data-toggle="tab" :href="'#'+offenceTab">Offence</a></li>
                            <li class="nav-item"><a data-toggle="tab" :href="'#'+detailsTab">Details</a></li>
                            <!-- li class="nav-item"><a data-toggle="tab" :href="'#'+documentTab">Document</a></li-->
                            <li class="nav-item"><a data-toggle="tab" :href="'#'+offenderTab">Offender(s)</a></li>
                            <li class="nav-item"><a data-toggle="tab" :href="'#'+locationTab" @click="mapOffenceClicked">Location</a></li>
                            <li class="nav-item"><a data-toggle="tab" :href="'#'+relatedItemsTab">Related Items</a></li>
                        </ul>
                        <div class="tab-content">
                            <div :id="offenceTab" class="tab-pane fade in active">
                                <FormSection :formCollapse="false" label="Offence" Index="0">

                                    <div class="col-sm-12 form-group"><div class="row">
                                        <div class="col-sm-3">
                                            <label class="control-label pull-left" for="offence-identifier">Identifier</label>
                                        </div>
                                        <div class="col-sm-6">
                                            <div v-if="offence">
                                                <input type="text" :readonly="readonlyForm" class="form-control" name="identifier" v-model="offence.identifier">
                                            </div>
                                        </div>
                                    </div></div>

                                    <div class="col-sm-12 form-group"><div class="row">
                                        <label class="col-sm-3">Use occurrence from/to</label>
                                        <input class="col-sm-1" :disabled="readonlyForm" id="occurrence_from_to_true" type="radio" v-model="offence.occurrence_from_to" v-bind:value="true">
                                        <label class="col-sm-1 radio-button-label" for="occurrence_from_to_true">Yes</label>
                                        <input class="col-sm-1" :disabled="readonlyForm" id="occurrence_from_to_false" type="radio" v-model="offence.occurrence_from_to" v-bind:value="false">
                                        <label class="col-sm-1 radio-button-label" for="occurrence_from_to_false">No</label>
                                    </div></div>

                                    <div class="col-sm-12 form-group"><div class="row">
                                        <label class="col-sm-3">{{ occurrenceDateLabel }}</label>
                                        <div class="col-sm-3">
                                            <div class="input-group date" ref="occurrenceDateFromPicker">
                                                <input :readonly="readonlyForm" type="text" class="form-control" placeholder="DD/MM/YYYY" :value="date_from" />
                                                <span class="input-group-addon">
                                                    <span class="glyphicon glyphicon-calendar"></span>
                                                </span>
                                            </div>
                                        </div>
                                        <div v-show="offence.occurrence_from_to">
                                            <div class="col-sm-3">
                                                <div class="input-group date" ref="occurrenceDateToPicker">
                                                    <input :readonly="readonlyForm" type="text" class="form-control" placeholder="DD/MM/YYYY" :value="date_to" />
                                                    <span class="input-group-addon">
                                                        <span class="glyphicon glyphicon-calendar"></span>
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    </div></div>

                                    <div class="col-sm-12 form-group"><div class="row">
                                        <label class="col-sm-3">{{ occurrenceTimeLabel }}</label>
                                        <div class="col-sm-3">
                                            <div class="input-group date" ref="occurrenceTimeFromPicker">
                                                <input :readonly="readonlyForm" type="text" class="form-control" placeholder="HH:MM" :value="time_from" />
                                                <span class="input-group-addon">
                                                    <span class="glyphicon glyphicon-calendar"></span>
                                                </span>
                                            </div>
                                        </div>
                                        <div v-show="offence.occurrence_from_to">
                                            <div class="col-sm-3">
                                                <div class="input-group date" ref="occurrenceTimeToPicker">
                                                    <input :readonly="readonlyForm" type="text" class="form-control" placeholder="HH:MM" :value="time_to" />
                                                    <span class="input-group-addon">
                                                        <span class="glyphicon glyphicon-calendar"></span>
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    </div></div>

                                    <div class="col-sm-12 form-group"><div class="row">
                                        <label class="col-sm-3">Alleged Offence</label>
                                        <div v-show="!readonlyForm">
                                            <div class="col-sm-6">
                                                <input class="form-control" id="alleged-offence" />
                                            </div>
                                            <div class="col-sm-3">
                                                <input type="button" class="btn btn-primary" value="Add" @click.prevent="addAllegedOffenceClicked()" />
                                            </div>
                                        </div>
                                    </div></div>

                                    <div class="col-sm-12 form-group"><div class="row">
                                        <div class="col-sm-12">
                                            <datatable parentStyle=" " ref="alleged_offence_table" id="alleged-offence-table" :dtOptions="dtOptionsAllegedOffence" :dtHeaders="dtHeadersAllegedOffence" />
                                        </div>
                                    </div></div>
                                </FormSection>
                            </div>
                            <div :id="detailsTab" class="tab-pane face in">
                                <FormSection :formCollapse="false" label="Details" Index="1">
                                    <textarea :readonly="readonlyForm" class="form-control" placeholder="add details" v-model="offence.details" />
                                </FormSection>
                            </div>
                            <div :id="documentTab" class="tab-pane face in">
                                <FormSection :formCollapse="false" label="Document" Index="1.5">
                                    <div class="form-group">
                                        <div class="row">
                                            <div class="col-sm-3">
                                                <label class="control-label pull-left"  for="Name">Attachments</label>
                                            </div>
                                            <div class="col-sm-9">
                                                <!--
                                                <FileField 
                                                    ref="comms_log_file" 
                                                    name="comms-log-file" 
                                                    :isRepeatable="true" 
                                                    documentActionUrl="temporary_document" 
                                                    @update-temp-doc-coll-id="setTemporaryDocumentCollectionId"
                                                />
                                                -->
                                            </div>
                                        </div>
                                    </div>
                                </FormSection>
                            </div>
                            <div :id="offenderTab" class="tab-pane face in">
                                <FormSection :formCollapse="false" label="Offender(s)" Index="2">
                                    <!--div class="col-sm-12 form-group"><div class="row">
                                        <input :disabled="readonlyForm" class="col-sm-1" id="offender_individual" type="radio" v-model="offender_search_type" value="individual">
                                        <label class="col-sm-1 radio-button-label" for="offender_individual">Individual</label>
                                        <input :disabled="readonlyForm" class="col-sm-1" id="offender_organisation" type="radio" v-model="offender_search_type" value="organisation">
                                        <label class="col-sm-1 radio-button-label" for="offender_organisation">Organisation</label>
                                    </div></div-->

                                    <div class="col-sm-12 form-group"><div class="row">
                                        <label class="col-sm-2">Offender</label>
                                        <div v-show="!readonlyForm">
                                            <div>
                                                <SearchPersonOrganisation
                                                :excludeStaff="true"
                                                :personOnly="true"
                                                classNames="form-control"
                                                @entity-selected="personSelected"
                                                showCreateUpdate
                                                ref="search_offender"
                                                domIdHelper="offender"
                                                v-bind:key="updateSearchPersonOrganisationBindId"/>
                                                <!--PersonSearch ref="person_search" elementId="idSetInParent" classNames="col-sm-5 form-control" @person-selected="personSelected" :search_type="offender_search_type" /-->
                                            </div>
                                            <div>
                                                <input type="button" class="btn btn-primary" value="Add to Offender List" @click.prevent="addOffenderClicked()" />
                                            </div>
                                            <!--div class="col-sm-2">
                                                <input type="button" class="btn btn-primary" value="Create New Person" @click.prevent="createNewPersonClicked()" />
                                            </div-->
                                        </div>
                                    </div></div>

                                    <div class="form-group"><div class="row">
                                        <!--div class="col-sm-12">
                                          <CreateNewPerson :displayComponent="displayCreateNewPerson" @new-person-created="newPersonCreated"/>
                                        </div-->

                                        <div class="col-sm-12">
                                            <datatable ref="offender_table" id="offender-table" :dtOptions="dtOptionsOffender" :dtHeaders="dtHeadersOffender" />
                                        </div>
                                    </div></div>

                                </FormSection>
                            </div>
                            <div :id="locationTab" class="tab-pane face in">
                                <FormSection :formCollapse="false" label="Location" Index="3">
                                    <MapLocation
                                        v-if="offence.location"
                                        :key="locationTab"
                                        ref="mapLocationComponent"
                                        :readonly="readonlyForm"
                                        :marker_longitude="offence.location.geometry.coordinates[0]"
                                        :marker_latitude="offence.location.geometry.coordinates[1]"
                                        @location-updated="locationUpdated"
                                    />
                                    <div :id="idLocationFieldsAddress" v-if="offence.location">
                                        <div class="col-sm-12 form-group"><div class="row">
                                            <label class="col-sm-4">Street</label>
                                            <input class="form-control" v-model="offence.location.properties.street" readonly />
                                        </div></div>
                                        <div class="col-sm-12 form-group"><div class="row">
                                            <label class="col-sm-4">Town/Suburb</label>
                                            <input class="form-control" v-model="offence.location.properties.town_suburb" readonly />
                                        </div></div>
                                        <div class="col-sm-12 form-group"><div class="row">
                                            <label class="col-sm-4">State</label>
                                            <input class="form-control" v-model="offence.location.properties.state" readonly />
                                        </div></div>
                                        <div class="col-sm-12 form-group"><div class="row">
                                            <label class="col-sm-4">Postcode</label>
                                            <input class="form-control" v-model="offence.location.properties.postcode" readonly />
                                        </div></div>
                                        <div class="col-sm-12 form-group"><div class="row">
                                            <label class="col-sm-4">Country</label>
                                            <input class="form-control" v-model="offence.location.properties.country" readonly />
                                        </div></div>
                                    </div>

                                    <div :id="idLocationFieldsDetails" v-if="offence.location">
                                        <div class="col-sm-12 form-group"><div class="row">
                                            <label class="col-sm-4">Details</label>
                                            <textarea class="form-control location_address_field" v-model="offence.location.properties.details" />
                                        </div></div>
                                    </div>
                                </FormSection>
                            </div>
                            <div :id="relatedItemsTab" class="tab-pane face in">
                                <FormSection :formCollapse="false" label="Related Items" Index="4">
                                    <div class="col-sm-12 form-group"><div class="row">
                                        <div class="col-sm-12">
                                            <RelatedItems v-bind:key="relatedItemsBindId" :parent_update_related_items="setRelatedItems" :readonlyForm="readonlyForm" />
                                        </div>
                                    </div></div>
                                </FormSection>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="visibilitySaveButton" class="navbar navbar-fixed-bottom" style="background-color: #f5f5f5 ">
            <div class="navbar-inner">
                <div class="container">
                    <p class="pull-right" style="margin-top:5px;">
                        <input type="button" @click.prevent="saveExit" class="btn btn-primary" value="Save and Exit"/>
                        <input type="button" @click.prevent="save" class="btn btn-primary" value="Save and Continue"/>
                    </p>
                </div>
            </div>
        </div>

        <div v-if="workflow_type">
            <OffenceWorkflow ref="add_workflow" :workflow_type="workflow_type" v-bind:key="workflowBindId" />
        </div>

        <div v-if="sanctionOutcomeInitialised">
            <SanctionOutcome ref="sanction_outcome" :parent_update_function="constructOffenceDedicatedPage" @sanction_outcome_created="constructOffenceDedicatedPage" />
        </div>
    </div>
</template>


<script>
import Vue from "vue";
import FormSection from "@/components/forms/section_toggle.vue";
import Assignment from "../assignment.vue";
import datatable from '@vue-utils/datatable.vue'
import utils from "../utils";
import { api_endpoints, helpers, cache_helper } from "@/utils/hooks";
import { mapState, mapGetters, mapActions, mapMutations } from "vuex";
import CommsLogs from "@common-components/comms_logs.vue";
import FileField from '@/components/common/compliance_file.vue';
import OffenceWorkflow from './offence_workflow';
import SearchPersonOrganisation from "@common-components/search_person_or_organisation.vue";
//import CreateNewPerson from "@common-components/create_new_person.vue";
import MapLocation from "../../common/map_location";
import SanctionOutcome from '../sanction_outcome/sanction_outcome_modal';
//import 'bootstrap/dist/css/bootstrap.css';
import "awesomplete/awesomplete.css";
import RelatedItems from "@common-components/related_items.vue";
import moment from 'moment';
import { v4 as uuidv4 } from 'uuid';
import hash from 'object-hash';

export default {
    name: 'ViewOffence',
    data() {
        let vm = this;
        vm.STATUS_DRAFT = 'draft';
        vm.STATUS_CLOSING = 'closing';
        vm.STATUS_CLOSED = 'closed';
        vm.STATUS_OPEN = 'open';
        vm.STATUS_DISCARDED = 'discarded';

        vm.max_items = 20;
        vm.ajax_for_alleged_offence = null;
        vm.ajax_for_offender = null;
        vm.suggest_list = []; // This stores a list of alleged offences displayed after search.
        vm.suggest_list_offender = []; // This stores a list of alleged offences displayed after search.
        vm.awe = null;

        return {
            mapboxAccessToken: null,
            uuid: 0,
            workflow_type :'',
            workflowBindId :'',
            offender_search_type: "individual",
            offenceTab: 'offenceTab' + vm._uid,
            detailsTab: 'detailsTab' + vm._uid,
            documentTab: 'documentTab' + vm._uid,
            offenderTab: 'offenderTab' + vm._uid,
            locationTab: 'locationTab' + vm._uid,
            relatedItemsTab: 'relatedItemsTab' + vm._uid,
            displayCreateNewPerson: false,
            idLocationFieldsAddress: vm.guid + "LocationFieldsAddress",
            idLocationFieldsDetails: vm.guid + "LocationFieldsDetails",
            sanctionOutcomeInitialised: false,
            objectHash : null,
            date_from: null,
            time_from: null,
            date_to: null,
            time_to: null,
            hashAttributeWhiteDict: {
                'alleged_offences': [
                    'id',
                    'reason_for_removal',
                    'removed',
                    'removed_by_id',
                    'section_regulation',
                ],
                'allocated_group_id': '__all__',
                'date_of_issue': '__all__',
                'details': '__all__',
                'district_id': '__all__',
                'identifier': '__all__',
                'location': '__all__',
                'lodgement_number': '__all__',
                'occurrence_date_from': '__all__',
                'occurrence_date_to': '__all__',
                'occurrence_time_from': '__all__',
                'occurrence_time_to': '__all__',
                'occurrence_from_to': '__all__',
                'offenders': [
                    'id',
                    'organisation',
                    'person',
                    'reason_for_removal',
                    'removed',
                    ,],
                'region_id': '__all__',
            },

            current_alleged_offence: {  // Store the alleged offence temporarily once selected in awesomplete. Cleared when clicking on the "Add" button.
                id: null,
                act: "",
                name: "",
                offence_text: ""
            },
            current_offender: null,  // Store the offender temporarily once selected in awesomplete. Cleared when clicking on the "Add" button.
            //offender_search_type: "individual",

            comms_url: helpers.add_endpoint_json(
                api_endpoints.offence,
                this.$route.params.offence_id + "/comms_log"
            ),
            comms_add_url: helpers.add_endpoint_json(
                api_endpoints.offence,
                this.$route.params.offence_id + "/add_comms_log"
            ),
            logs_url: helpers.add_endpoint_json(
                api_endpoints.offence,
                this.$route.params.offence_id + "/action_log"
            ),
            assign_url: helpers.add_endpoint_join(
                api_endpoints.offence,
                this.$route.params.offence_id + '/update_assigned_to_id/'
            ),
            assignmentKey: 0,
            dtHeadersOffender: [
                "id",
                "Individual/Organisation",
                "Details",
                "Action",
                "Reason for removal",
            ],
            dtHeadersAllegedOffence: [
                "id",
                "Act",
                "Section/Regulation",
                "Alleged Offence",
                "Action",
                "Reason for removal",
            ],
            dtOptionsOffender: {
                columns: [
                    {
                        visible: false,
                        data: 'offender',
                        render: function(data, type, row) {
                            return row.offender.id;
                        }
                    },
                    {
                        data: 'offender',
                        render: function(data, type, row) {
                            let data_type = '';
                            if (row.offender.person){
                                data_type = 'individual';
                            }
                            else {
                                data_type = 'organisation';
                            }
                            if(row.offender.removed){
                                data_type = '<strike>' + data_type + '</strike>';
                            }
                            return data_type;
                        }
                    },
                    {
                        data: 'offender',
                        render: function(data, type, row) {
                            if (row.offender.person) {
                                let full_name = [row.offender.person.first_name, row.offender.person.last_name].filter(Boolean).join(" ");
                                let email = row.offender.person.email ? "E:" + row.offender.person.email : "";
                                let p_number = row.offender.person.phone_number ? "P:" + row.offender.person.phone_number : "";
                                let m_number = row.offender.person.mobile_number ? "M:" + row.offender.person.mobile_number : "";
                                let dob = row.offender.person.dob ? "DOB:" + row.offender.person.dob : "DOB: ---";
                                let myLabel = ["<strong>" + full_name + "</strong>", email, p_number, m_number, dob].filter(Boolean).join("<br />");
                                if (row.offender.removed){
                                    myLabel = '<strike>' + myLabel + '</strike>';
                                }
                                return myLabel;
                            } else if (row.offender.organisation) {
                                let name = row.offender.organisation.name ? row.offender.organisation.name : "";
                                let abn = row.offender.organisation.abn ? "ABN:" + row.offender.organisation.abn : "";
                                let myLabel = ["<strong>" + name + "</strong>", abn].filter(Boolean).join("<br />");
                                if (row.offender.removed){
                                    myLabel = '<strike>' + myLabel + '</strike>';
                                }
                                return myLabel;
                            }
                        }
                    },
                    {
                        data: 'offender',
                        render: function(data, type, row) {
                            //let ret_str = row.offender.number_linked_sanction_outcomes_active + '(' + row.offender.number_linked_sanction_outcomes_total + ')';
                            let ret_str = '';
                            if (row.offence.in_editable_status && row.offence.can_user_action){
                                if (row.offender.removed){
                                    ret_str = ret_str + '<a href="#" class="restore_button" data-offender-uuid="' + row.offender.uuid + '">Restore</a>';
                                } else {
                                    if (!row.offender.number_linked_sanction_outcomes_active){
                                        ret_str = ret_str + '<a href="#" class="remove_button" data-offender-uuid="' + row.offender.uuid + '">Remove</a>';
                                    }
                                }
                            }
                            return ret_str;
                        }
                    },

                    {
                        data: 'offender',
                        render: function(data, type, row) {
                            let ret_str = '';
                            if (row.offender.removed){
                                if(row.offender.reason_for_removal){
                                    ret_str = ret_str + row.offender.reason_for_removal;
                                } else {
                                    ret_str = ret_str + '<textarea class="reason_element" data-offender-uuid="' + row.offender.uuid + '">' + row.offender.reason_for_removal + '</textarea>';
                                }
                            }
                            return ret_str;
                        }
                    }

                ]
            },
            dtOptionsAllegedOffence: {
                columns: [
                    {
                        visible: false,
                        data: 'allegedOffence',
                        render: function(data, type, row) {
                            return row.allegedOffence.id;
                        }
                    },
                    {
                        data: 'allegedOffence',
                        render: function(data, type, row) {
                            let ret_str = row.allegedOffence.section_regulation.act;
                            if (row.allegedOffence.removed) {
                                ret_str = '<strike>' + ret_str + '</strike>';
                            }
                            return ret_str;
                        }
                    },
                    {
                        data: 'allegedOffence',
                        render: function(data, type, row) {
                            let ret_str = row.allegedOffence.section_regulation.name;
                            if (row.allegedOffence.removed) {
                                ret_str = '<strike>' + ret_str + '</strike>';
                            }
                            return ret_str;
                        }
                    },
                    {
                        data: 'allegedOffence',
                        render: function(data, type, row) {
                            let ret_str = row.allegedOffence.section_regulation.offence_text;
                            if (row.allegedOffence.removed) {
                                ret_str = '<strike>' + ret_str + '</strike>';
                            }
                            return ret_str;
                        }
                    },
                    {
                        data: 'allegedOffence',
                        render: function(data, type, row) {
                            //let ret_str = row.allegedOffence.number_linked_sanction_outcomes_active + '/' + row.allegedOffence.number_linked_sanction_outcomes_total;
                            let ret_str = '';
                            if (row.offence.in_editable_status && row.offence.can_user_action){
                                if (row.allegedOffence.removed){
                                    ret_str = ret_str + '<a href="#" class="restore_button" data-alleged-offence-uuid="' + row.allegedOffence.uuid + '">Restore</a>';
                                } else {
                                    if (!row.allegedOffence.number_linked_sanction_outcomes_active){
                                        ret_str = ret_str + '<a href="#" class="remove_button" data-alleged-offence-uuid="' + row.allegedOffence.uuid + '">Remove</a>';
                                    }
                                }
                            }
                            return ret_str;

                        }
                    },
                    {
                        data: 'allegedOffence',
                        render: function(data, type, row) {
                            let ret_str = '';

                            let num_chars = 1000;
                            if (row.allegedOffence.removed){
                                if(row.allegedOffence.reason_for_removal){
                                    let name = row.allegedOffence.reason_for_removal;
                                    let shortText = (name.length > num_chars) ?
                                        '<span title="' + name + '">' + $.trim(name).substring(0, num_chars).split(" ").slice(0, -1).join(" ") + '...</span>' :
                                        name;
                                    ret_str = ret_str + shortText;

                                } else {
                                    ret_str = ret_str + '<textarea class="reason_element" data-alleged-offence-uuid="' + row.allegedOffence.uuid + '">' + row.allegedOffence.reason_for_removal + '</textarea>';
                                }
                            }
                            return ret_str;

                        }
                    }
                ]
            }
        }
    },
    components: {
        FormSection,
        OffenceWorkflow,
        CommsLogs,
        datatable,
        SearchPersonOrganisation,
        MapLocation,
        //CreateNewPerson,
        RelatedItems,
        SanctionOutcome,
        FileField,
        Assignment,
    },
    computed: {
        ...mapGetters('offenceStore', {
            offence: "offence",
        }),
        readonlyForm: function() {
            return !this.canUserEdit;
        },
        canUserEdit: function() {
            let visibility = false;
            if (this.canUserAction){
                if (this.offence.status.id === this.STATUS_DRAFT || this.offence.status.id === this.STATUS_OPEN){
                    visibility = true;
                }
            }
            return visibility;
        },
        updateSearchPersonOrganisationBindId: function() {
            this.uuid += 1
            return 'offender' + this.uuid
        },
        occurrenceDateLabel: function() {
            if (this.offence.occurrence_from_to) {
                return "Occurrence date from";
            } else {
                return "Occurrence date";
            }
        },
        occurrenceTimeLabel: function() {
            if (this.offence.occurrence_from_to) {
                return "Occurrence time from";
            } else {
                return "Occurrence time";
            }
        },
        statusDisplay: function() {
            let ret = '';
            if (this.offence){
                if (this.offence.status){
                    ret = this.offence.status.name;
                }
            }
            return ret;
        },
        displayLodgementNumber: function() {
            let ret = '';
            if (this.offence){
                ret = this.offence.lodgement_number;
            }
            return ret;
        },
        canUserAction: function() {
            return this.offence.can_user_action;
        },
        visibilitySaveButton: function() {
            let visibility = false;
            if (this.canUserAction){
                if (this.offence.status.id === this.STATUS_DRAFT || this.offence.status.id === this.STATUS_OPEN){
                    visibility = true;
                }
            }
            return visibility;
        },
        visibilitySanctionOutcomeButton: function() {
            let visibility = false;
            let num_offenders = 0;
            if (this.offence.offenders && this.offence.offenders.length){
                num_offenders = this.offence.offenders.length;
            }
            if (this.canUserAction){
                if (this.offence.status.id === this.STATUS_OPEN){
                    for (let i=0; i<this.offence.alleged_offences.length; i++){
                        let alleged_offence = this.offence.alleged_offences[i];
                        //if (alleged_offence.connected_offenders.length < num_offenders){
                            visibility = true;
                            break;
                        //}
                    }
                }
            }
            return visibility;
        },
        visibilityCloseButton: function() {
            let visibility = false;
            if (this.canUserAction){
                if (this.offence.status.id === this.STATUS_OPEN){
                    visibility = true;
                }
            }
            return visibility;
        },
        relatedItemsBindId: function() {
            let timeNow = Date.now()
            if (this.offence && this.offence.id) {
                return 'offence_' + this.offence.id + '_' + this._uid;
            } else {
                return timeNow.toString();
            }
        },
    },
    methods: {
        ...mapActions('offenceStore', {
            loadOffenceVuex: 'loadOffence',
            saveOffence: 'saveOffence',
            setOffence: 'setOffence',
            setAssignedToId: 'setAssignedToId',
            setCanUserAction: 'setCanUserAction',
            setRelatedItems: 'setRelatedItems',
        }),
        setTemporaryDocumentCollectionId: function(val) {
            this.temporary_document_collection_id = val;
        },
        constructOffenceDedicatedPage: async function(){
            console.log('constructOffenceDedicatedPage');
            await this.loadOffenceVuex({offence_id: this.$route.params.offence_id});
            if (this.offence.occurrence_datetime_from){
                this.date_from = moment(this.offence.occurrence_datetime_from).format("DD/MM/YYYY");
                this.time_from = moment(this.offence.occurrence_datetime_from).format("LT");
                console.log('date_from and time_from has been set');
            }
            if (this.offence.occurrence_datetime_to){
                this.date_to = moment(this.offence.occurrence_datetime_to).format("DD/MM/YYYY");
                this.time_to = moment(this.offence.occurrence_datetime_to).format("LT");
                console.log('date_to and time_to has been set');
            }
            this.constructAllegedOffencesTable();
            this.constructOffendersTable();
            this.updateObjectHash();
        },
        updateObjectHash: function() {
            this.objectHash = this.calculateHash();
        },
        calculateHash: function() {
            console.log('calculateHash()');
            console.log(this.offence);

            let copiedObject = {}
            Object.getOwnPropertyNames(this.offence).forEach(
                (val, idx, array) => {
                    if(val in this.hashAttributeWhiteDict){
                        let attributes = this.hashAttributeWhiteDict[val];  // Array or '__all__'
                        let target_obj = this.offence[val];  // Can be array

                        if (attributes == '__all__'){
                            copiedObject[val] = target_obj;
                        }
                        else if (Array.isArray(target_obj)){
                            for (let j=0; j<target_obj.length; j++){
                                let target = target_obj[j];
                                for (let i=0; i<attributes.length; i++){
                                    copiedObject[val + j.toString() + i.toString()] = target[attributes[i]];
                                }
                            }
                        }
                        else {
                            for (let i=0; i<attributes.length; i++){
                                copiedObject[val + i.toString()] = target_obj[attributes[i]];
                            }
                        }
                    }
                });
            let hashedValue = hash(copiedObject);
            console.log(hashedValue);
            return hashedValue;
        },
        formChanged: function(){
            let changed = false;
            if (!this.readonlyForm){
                if(this.objectHash !== this.calculateHash()){
                    changed = true;
                }
            }
            return changed;
        },
        save: async function(){
            try {
                console.log('aho');
                console.log($(this.$refs.occurrenceDateFromPicker).data('DateTimePicker').date());
                await this.saveOffence({'fr_date': this.date_from, 'fr_time': this.time_from, 'to_date': this.date_to, 'to_time': this.time_to});
                await swal("Saved", "The record has been saved", "success");

                this.constructOffendersTable();
                this.constructAllegedOffencesTable();
                this.updateObjectHash();
            } catch (err) {
                console.log('aho')
                this.processError(err);
            }
        },
        leaving: function(e) {
            let dialogText = 'You have some unsaved changes.';
            if (this.formChanged()){
                e.returnValue = dialogText;
                return dialogText;
            }
        },
        destroyed: function() {
            window.removeEventListener('beforeunload', this.leaving);
            window.removeEventListener('onblur', this.leaving);
        },
        saveExit: async function() {
            try {
                //await this.saveOffence();
                await this.saveOffence({'fr_date': this.date_from, 'fr_time': this.time_from, 'to_date': this.date_to, 'to_time': this.time_to});
                await swal("Saved", "The record has been saved", "success");

                // remove redundant eventListeners
                window.removeEventListener('beforeunload', this.leaving);
                window.removeEventListener('onblur', this.leaving);

                this.$router.push({ name: 'internal-offence-dash' });
            } catch (err) {
                this.processError(err);
            }
        },
        processError: async function(err){
            let errorText = '';
            if (err.body){
                if (err.body.non_field_errors) {
                    // When non field errors raised
                    for (let i=0; i<err.body.non_field_errors.length; i++){
                        errorText += err.body.non_field_errors[i] + '<br />';
                    }
                } else if(Array.isArray(err.body)) {
                    // When general errors raised
                    for (let i=0; i<err.body.length; i++){
                        errorText += err.body[i] + '<br />';
                    }
                } else {
                    // When field errors raised
                    for (let field_name in err.body){
                        if (err.body.hasOwnProperty(field_name)){
                            errorText += field_name + ':<br />';
                            for (let j=0; j<err.body[field_name].length; j++){
                                errorText += err.body[field_name][j] + '<br />';
                            }
                        }
                    }
                }
            } else {
                errorText += err.message;
            }
            await swal("Error", errorText, "error");
        },
        updateAssignedToId: async function (body) {
            //this.setAssignedToId(body.assigned_to_id);
            //this.setCanUserAction(body.can_user_action);
            this.setOffence(body);
            this.constructOffendersTable();
            this.constructAllegedOffencesTable();
            this.updateObjectHash();
            this.assignmentKey += 1;
        },
        openSanctionOutcome: async function() {
            try {
                if (this.formChanged()){
                    // Save changes implicitly
                    //await this.saveOffence();
                    await this.saveOffence({'fr_date': this.date_from, 'fr_time': this.time_from, 'to_date': this.date_to, 'to_time': this.time_to});
                    this.updateObjectHash();
                }
                this.sanctionOutcomeInitialised = true;
                this.$nextTick(() => {
                    this.$refs.sanction_outcome.isModalOpen = true;
                });
            } catch (err) {
                this.processError(err);
            }
        },
        updateWorkflowBindId: function() {
            let timeNow = Date.now()
            if (this.workflow_type) {
                this.workflowBindId = this.workflow_type + '_' + timeNow.toString();
            } else {
                this.workflowBindId = timeNow.toString();
            }
        },
        addWorkflow: async function(workflow_type) {
            try {
                if (this.formChanged()){
                    // Save changes implicitly
                    //await this.saveOffence();
                    await this.saveOffence({'fr_date': this.date_from, 'fr_time': this.time_from, 'to_date': this.date_to, 'to_time': this.time_to});
                    this.updateObjectHash();
                }
                this.workflow_type = workflow_type;
                this.updateWorkflowBindId();
                this.$nextTick(() => {
                    this.$refs.add_workflow.isModalOpen = true;
                });
            } catch (err) {
                this.processError(err);
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
            if (this.offence.location){
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
                  this.offence.location.properties.street = address_arr[0];

                  /*
                   * Split the string into suburb, state and postcode
                   */
                  let reg = /^([a-zA-Z0-9\s]*)\s(New South Wales|Queensland|South Australia|Tasmania|Victoria|Western Australia|Northern Territory|Australian Capital Territory){1}\s+(\d{4})$/gi;
                  let result = reg.exec(address_arr[1]);
                  /* suburb */
                  this.offence.location.properties.town_suburb = result[1].trim();

                  /* state */
                  let state_abbr = state_abbr_list[result[2].trim()];
                  this.offence.location.properties.state = state_abbr;

                  /* postcode */
                  this.offence.location.properties.postcode = result[3].trim();
                  /* country */

                  this.offence.location.properties.country = "Australia";
            }
        },
        setLocationAddressEmpty() {
            if(this.offence.location){
                this.offence.location.properties.town_suburb = "";
                this.offence.location.properties.street = "";
                this.offence.location.properties.state = "";
                this.offence.location.properties.postcode = "";
                this.offence.location.properties.country = "";
            }
        },
        setLocationDetailsFieldEmpty() {
            if(this.offence.location){
                this.offence.location.properties.details = "";
            }
        },
        locationUpdated: function(latlng){
            // Update coordinate
            this.offence.location.geometry.coordinates[1] = latlng.lat;
            this.offence.location.geometry.coordinates[0] = latlng.lng;
            // Update Address/Details
            this.reverseGeocoding(latlng);
        },
        mapOffenceClicked: function() {
            // Call this function to render the map correctly
            // In some case, leaflet map is not rendered correctly...   Just partialy shown...
            if(this.$refs.mapLocationComponent){
                this.$refs.mapLocationComponent.invalidateSize();
            }
        },
        //newPersonCreated: function(obj) {
        //  if(obj.person){
        //    this.setCurrentOffender('individual', obj.person.id);

        //    // Set fullname and DOB into the input box
        //    let full_name = [obj.person.first_name, obj.person.last_name].filter(Boolean).join(" ");
        //    let dob = obj.person.dob ? "DOB:" + obj.person.dob : "DOB: ---";
        //    let value = [full_name, dob].filter(Boolean).join(", ");
        //    this.$refs.search_offender.setInput(value);
        //  } else if (obj.err) {
        //    console.log(err);
        //  } else {
        //    // Should not reach here
        //  }
        //},
        personSelected: function(para) {
            let vm = this;
            vm.setCurrentOffender(para.data_type, para.id);
        },
        createNewPersonClicked: function() {
          let vm = this;
          vm.newPersonBeingCreated = true;
          vm.displayCreateNewPerson = !vm.displayCreateNewPerson;
        },
        cancelCreateNewPersonClicked: function() {
          let vm = this;
          vm.newPersonBeingCreated = false;
        },
        saveNewPersonClicked: function() {
          let vm = this;
          vm.newPersonBeingCreated = false;
        },

        reasonOffenderLostFocus: function(e) {
            let offender_uuid = e.target.getAttribute("data-offender-uuid");

            for (let i=0; i<this.offence.offenders.length; i++){
                let offender = this.offence.offenders[i];
                if (offender.uuid == offender_uuid){
                    offender.reason_for_removal = e.target.value;
                }
            }
        },
        reasonAllegedOffenceLostFocus: function(e) {
            let alleged_offence_uuid = e.target.getAttribute("data-alleged-offence-uuid");

            for (let i=0; i<this.offence.alleged_offences.length; i++){
                let alleged_offence = this.offence.alleged_offences[i];
                if (alleged_offence.uuid == alleged_offence_uuid){
                    alleged_offence.reason_for_removal = e.target.value;
                }
            }
        },
        removeOffenderClicked: function(e) {
            let offender_uuid = e.target.getAttribute("data-offender-uuid");

            // Remove offender
            for (let i=0; i<this.offence.offenders.length; i++){
                let offender = this.offence.offenders[i];
                if (offender.uuid == offender_uuid){
                    if (offender.id){
                        // this offender exists in the database
                        offender.removed = true;
                    } else {
                        // this is new offender
                        this.offence.offenders.splice(i, 1);
                    }
                }
            }
            this.constructOffendersTable();
        },
        restoreOffenderClicked: function(e){
            let offender_uuid = e.target.getAttribute("data-offender-uuid");

            // Restore offender
            for (let i=0; i<this.offence.offenders.length; i++){
                let offender = this.offence.offenders[i];
                if (offender.uuid == offender_uuid){
                    if (offender.id){
                        // this offender exists in the database
                        offender.removed = false;
                    } else {
                        // this is new offender
                        // Should not reach here
                    }
                }
            }
            this.constructOffendersTable();
        },
        restoreAllegedOffenceClicked: function(e) {
            let alleged_offence_uuid = e.target.getAttribute("data-alleged-offence-uuid");

            // Restore alleged_offence
            for (let i=0; i<this.offence.alleged_offences.length; i++){
                let alleged_offence = this.offence.alleged_offences[i];
                if (alleged_offence.uuid == alleged_offence_uuid){
                    if (alleged_offence.id){
                        // this alleged_offence exists in the database
                        alleged_offence.removed = false;
                    } else {
                        // this is new alleged_offence
                        // Should not reach here
                    }
                }
            }
            this.constructAllegedOffencesTable();
        },
        removeAllegedOffenceClicked: function(e) {
            let alleged_offence_uuid = e.target.getAttribute("data-alleged-offence-uuid");

            // Remove offender
            for (let i=0; i<this.offence.alleged_offences.length; i++){
                let alleged_offence = this.offence.alleged_offences[i];
                if (alleged_offence.uuid == alleged_offence_uuid){
                    if (alleged_offence.id){
                        // this alleged_offence exists in the database
                        alleged_offence.removed = true;
                    } else {
                        // this is new alleged_offence
                        this.offence.alleged_offences.splice(i, 1);
                    }
                }
            }
            this.constructAllegedOffencesTable();
        },
        addOffenderClicked: async function() {
            if (this.current_offender && this.current_offender.id && this.current_offender.data_type) {
                // save person before adding to offender list
                await this.$refs.search_offender.parentSave()

                // Check if the item is already in the list
                let already_exists = false;
                for (let i=0; i<this.offence.offenders.length; i++){
                    let offender = this.offence.offenders[i];
                    if (this.current_offender.data_type == 'individual'){
                        if (offender.person){
                            if (!offender.removed && offender.person.id == this.current_offender.id){
                                already_exists = true;
                            }
                        }
                    } else if (this.current_offender.data_type == 'organisation'){
                        if (offender.organisation){
                            if (!offender.removed && offender.organisation.id == this.current_offender.id){
                                already_exists = true;
                            }
                        }
                    }
                }

                if (!already_exists) {
                    let offender_obj = {
                        id: '',
                        can_user_action: true,
                        removed: false,
                        reason_for_removal: '',
                        person: null,
                        organisation: null,
                        number_linked_sanction_outcomes_total: 0,
                        number_linked_sanction_outcomes_active: 0,
                        uuid: uuidv4()
                    };
                    if (this.current_offender.data_type == 'individual'){
                        // Add person as offender object
                        offender_obj['person'] = this.current_offender;
                    } else if (this.current_offender.data_type == 'organisation'){
                        // Add organisation as offender object
                        offender_obj['organisation'] = this.current_offender;
                    }
                    this.offence.offenders.push(offender_obj);
                }
            }
            this.constructOffendersTable();
            this.setCurrentOffenderEmpty();
        },
        addAllegedOffenceClicked: function() {
            if (this.current_alleged_offence && this.current_alleged_offence.id) {

                // Check if the item is already in the list
                let already_exists = false;
                for (let i=0; i<this.offence.alleged_offences.length; i++){
                    let alleged_offence = this.offence.alleged_offences[i];
                    if(alleged_offence.section_regulation.id == this.current_alleged_offence.id){
                        already_exists = true;
                    }
                }

                if (!already_exists) {
                    let alleged_offence_obj = {
                        id: '',
                        removed: false,
                        reason_for_removal: '',
                        removed_by_id: null,
                        section_regulation: this.current_alleged_offence,
                        number_linked_sanction_outcomes_total: 0,
                        number_linked_sanction_outcomes_active: 0,
                        uuid: uuidv4()
                    };
                    this.offence.alleged_offences.push(alleged_offence_obj);
                }
            }

            this.constructAllegedOffencesTable();
            this.setCurrentAllegedOffenceEmpty();
        },
        constructAllegedOffencesTable: function(){
            this.$refs.alleged_offence_table.vmDataTable.clear().draw();
            if (this.offence.alleged_offences){
                for(let i=0; i<this.offence.alleged_offences.length; i++){
                    this.addAllegedOffenceToTable(this.offence.alleged_offences[i]);
                }
            }
        },
        addAllegedOffenceToTable: function(allegedOffence){
            allegedOffence.uuid = uuidv4();
            this.$refs.alleged_offence_table.vmDataTable.row.add({ allegedOffence: allegedOffence, offence: this.offence }).draw();
        },
        constructOffendersTable: function(){
            this.$refs.offender_table.vmDataTable.clear().draw();
            if (this.offence.offenders){
                for(let i=0; i<this.offence.offenders.length; i++){
                    this.addOffenderToTable(this.offence.offenders[i]);
                }
            }
        },
        addOffenderToTable: function(offender) {
            offender.uuid = uuidv4();
            this.$refs.offender_table.vmDataTable.row.add({ offender: offender, offence: this.offence }).draw();
        },
        markMatchedText(original_text, input) {
          let ret_text = original_text.replace(new RegExp(input, "gi"), function(a, b) {
            return "<mark>" + a + "</mark>";
          });
          return ret_text;
        },
        initAwesompleteAllegedOffence: function() {
          var self = this;

          var element_search = document.getElementById("alleged-offence");
          self.awe = new Awesomplete(element_search, {
            maxItems: self.max_items,
            sort: false,
            filter: () => {
              return true;
            }, // Display all the items in the list without filtering.
            item: function(text, input) {
              let ret = Awesomplete.ITEM(text, ""); // Not sure how this works but this doesn't add <mark></mark>
              return ret;
            },
            data: function(item, input) {
              let act = item.act ? item.act : "";
              let name = item.name ? item.name : "";
              let offence_text = item.offence_text ? item.offence_text : "";

              let act_marked = self.markMatchedText(act, input);
              let name_marked = self.markMatchedText(name, input);
              let offence_text_marked = self.markMatchedText(offence_text, input);

              let myLabel = [
                "<strong>" + act_marked + ", " + name_marked + "</strong>",
                offence_text_marked
              ]
                .filter(Boolean)
                .join("<br />");
              myLabel = '<div data-item-id="' + item.id + '">' + myLabel + "</div>";

              return {
                label: myLabel, // Displayed in the list below the search box
                value: [act, name, offence_text].filter(Boolean).join(", "), // Inserted into the search box once selected
                id: item.id
              };
            }
          });
          $(element_search)
            .on("keyup", function(ev) {
              var keyCode = ev.keyCode || ev.which;
              if (
                (48 <= keyCode && keyCode <= 90) ||
                (96 <= keyCode && keyCode <= 105) ||
                keyCode == 8 ||
                keyCode == 46
              ) {
                self.search(ev.target.value);
                return false;
              }
            })
            .on("awesomplete-selectcomplete", function(ev) {
              ev.preventDefault();
              ev.stopPropagation();
              return false;
            })
            .on("awesomplete-select", function(ev) {
              /* Retrieve element id of the selected item from the list
               * By parsing it, we can get the order-number of the item in the list
               */
              let origin = $(ev.originalEvent.origin);
              let originTagName = origin[0].tagName;
                switch(originTagName){
                    case "STRONG":
                        origin = origin.parent();
                        break;
                    case "MARK":
                        origin = origin.parent().parent();
                        break;
                    case "LI":
                        origin = origin.children().first();
                        break;
                }
              let elem_id = origin[0].getAttribute("data-item-id");
              for (let i = 0; i < self.suggest_list.length; i++) {
                if (self.suggest_list[i].id == parseInt(elem_id)) {
                  self.setCurrentOffenceSelected(self.suggest_list[i]);
                  break;
                }
              }
            });
        },
        search: function(searchTerm) {
          var vm = this;
          vm.suggest_list = [];
          vm.suggest_list.length = 0;
          vm.awe.list = [];

          /* Cancel all the previous requests */
          if (vm.ajax_for_alleged_offence != null) {
            vm.ajax_for_alleged_offence.abort();
            vm.ajax_for_alleged_offence = null;
          }

          vm.ajax_for_alleged_offence = $.ajax({
            type: "GET",
            url: "/api/search_alleged_offences/?search=" + searchTerm,
            success: function(data) {
              if (data && data.results) {
                let persons = data.results;
                let limit = Math.min(vm.max_items, persons.length);
                for (var i = 0; i < limit; i++) {
                  vm.suggest_list.push(persons[i]);
                }
              }
              vm.awe.list = vm.suggest_list;
              vm.awe.evaluate();
            },
            error: function(e) {}
          });
        },
        searchOrganisation: function(id) {
          return new Promise((resolve, reject) => {
            Vue.http.get("/api/search_organisation/" + id).then(
              response => {
                resolve(response.body);
              },
              error => {
                reject(error);
              }
            );
          });
        },
        setCurrentOffender: function(data_type, id) {
          let vm = this;
          if (!id) {
              this.current_offender = null;
          } else if (data_type == "individual") {
            let initialisers = [utils.fetchUser(id)];
            Promise.all(initialisers).then(data => {
              vm.current_offender = data[0];
              vm.current_offender.data_type = "individual";
            });
          } else if (data_type == "organisation") {
            let initialisers = [vm.searchOrganisation(id)];
            Promise.all(initialisers).then(data => {
              vm.current_offender = data[0];
              vm.current_offender.data_type = "organisation";
            });
          }
        },
        setCurrentOffenceSelected: function(offence) {
          let vm = this;

          if (offence.id) {
            vm.current_alleged_offence.id = offence.id;
            vm.current_alleged_offence.act = offence.act;
            vm.current_alleged_offence.name = offence.name;
            vm.current_alleged_offence.offence_text = offence.offence_text;
          } else {
            vm.setCurrentAllegedOffenceEmpty();
          }
        },
        setCurrentOffenderEmpty: function() {
            this.current_offender = {};
            $("#offender_input").val("");
            this.$refs.search_offender.clearInput();
        },
        setCurrentAllegedOffenceEmpty: function() {
            this.current_alleged_offence = {};
            $("#alleged-offence").val("");
        },
        addEventListeners: function() {
            console.log('addEventListeners');
            let vm = this;
            let el_fr_date = $(vm.$refs.occurrenceDateFromPicker);
            let el_fr_time = $(vm.$refs.occurrenceTimeFromPicker);
            let el_to_date = $(vm.$refs.occurrenceDateToPicker);
            let el_to_time = $(vm.$refs.occurrenceTimeToPicker);

            // "From" Date field
            el_fr_date.datetimepicker({
                format: "DD/MM/YYYY",
                maxDate: moment().millisecond(0).second(0).minute(0).hour(0),
                showClear: true,
                date: vm.offence.occurrence_datetime_from,
            });
            el_fr_date.on("dp.change", function(e) {
                if (el_fr_date.data("DateTimePicker").date()) {
                    vm.date_from = e.date.format('DD/MM/YYYY');
                    el_to_date.data("DateTimePicker").minDate(e.date);
                } else if (el_fr_date.data("date") === "") {
                    vm.date_from = null;
                }
            });
            // "From" Time field
            el_fr_time.datetimepicker({
                format: "LT",
                showClear: true,
                date: vm.offence.occurrence_datetime_from,
            });
            el_fr_time.on("dp.change", function(e) {
                if (el_fr_time.data("DateTimePicker").date()) {
                    vm.time_from = e.date.format('LT');
                } else if (el_fr_time.data("date") === "") {
                    vm.time_from = null;
                }
            });

            // "To" Date field
            console.log('to date');
            console.log(vm.offence.occurrence_datetime_from);

            el_to_date.datetimepicker({
                format: "DD/MM/YYYY",
                maxDate: moment().millisecond(0).second(0).minute(0).hour(0),
                minDate: vm.offence.occurrence_datetime_from,
                showClear: true,
                date: vm.offence.occurrence_datetime_to,
            });
            el_to_date.on("dp.change", function(e) {
                if (el_to_date.data("DateTimePicker").date()) {
                    vm.date_to = e.date.format('DD/MM/YYYY');
                    //el_fr_date.data("DateTimePicker").maxDate(e.date);
                } else if (el_to_date.data("date") === "") {
                    vm.date_to = null;
                }
            });
            // "To" Time field
            el_to_time.datetimepicker({
                format: "LT",
                showClear: true,
                date: vm.offence.occurrence_datetime_to,
            });
            el_to_time.on("dp.change", function(e) {
                if (el_to_time.data("DateTimePicker").date()) {
                    vm.time_to = e.date.format('LT');
                } else if (el_to_time.data("date") === "") {
                    vm.time_to = null;
                }
            });

            $("#alleged-offence-table").on("click", ".remove_button", vm.removeAllegedOffenceClicked);
            $("#alleged-offence-table").on("click", ".restore_button", vm.restoreAllegedOffenceClicked);
            $("#alleged-offence-table").on("blur", ".reason_element", vm.reasonAllegedOffenceLostFocus);

            $("#offender-table").on("click", ".remove_button", vm.removeOffenderClicked);
            $("#offender-table").on("click", ".restore_button", vm.restoreOffenderClicked);
            $("#offender-table").on("blur", ".reason_element", vm.reasonOffenderLostFocus);

            window.addEventListener('beforeunload', this.leaving);
            window.addEventListener('onblur', this.leaving);
        },
    },
    created: async function() {
        let temp_token = await this.retrieveMapboxAccessToken();
        this.mapboxAccessToken = temp_token.access_token;

        if (this.$route.params.offence_id) {
            await this.constructOffenceDedicatedPage();
        }
        this.$nextTick(function() {
            this.initAwesompleteAllegedOffence();
        });
    },
    mounted: async function() {
        console.log('mounted');
        let vm = this;

        vm.$nextTick(() => {
            vm.addEventListeners();
        });
    }
}
</script>

<style>

</style>
