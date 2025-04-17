<template lang="html">
    <div class="container">
      <div class="row">
        <div class="col-md-3">
          <h3>Case: {{ legal_case.number }}</h3>
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
                        :user_is_assignee="legal_case.user_is_assignee"
                        :allowed_group_ids="legal_case.allowed_groups"
                        :user_in_group="legal_case.user_in_group" 
                        :assigned_to_id="legal_case.assigned_to_id" 
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
                        <div class="row">
                            <div v-if="canUserAction && openStatus" class="col-sm-12 action-button">
                                  <a @click="openInspection()" class="btn btn-primary btn-block" >
                                    Inspection
                                  </a>
                            </div>
                        </div>
                        <div class="row">
                          <div v-if="canUserAction && openStatus" class="col-sm-12 action-button">
                                <a @click="openOffence()" class="btn btn-primary btn-block">
                                  Offence
                                </a>
                          </div>
                        </div>
                        <div class="row">
                          <div v-if="canUserAction && openStatus" class="col-sm-12 action-button">
                                <input
                                :disabled="!sanctionOutcomeVisibility"
                                type="button"
                                class="btn btn-primary btn-block"
                                value="Sanction Outcome"
                                @click.prevent="openSanctionOutcome()"
                                />
                          </div>
                        </div>

                        <div  class="row">
                          <div v-if="canUserAction && openStatus" class="col-sm-12 action-button">
                                <a @click="addWorkflow('brief_of_evidence')" class="btn btn-primary btn-block">
                                <!--a @click="createBriefOfEvidence" class="btn btn-primary btn-block"-->
                                  Brief of Evidence
                                </a>
                          </div>
                        </div>
                        <div  class="row">
                          <div v-if="canUserAction && briefOfEvidenceStatus" class="col-sm-12 action-button">
                                <a @click="addWorkflow('back_to_case')" class="btn btn-primary btn-block">
                                <!--a @click="createProsecutionBrief" class="btn btn-primary btn-block"-->
                                  Back To Case
                                </a>
                          </div>
                        </div>
                        <div  class="row">
                          <div v-if="canUserAction && briefOfEvidenceVisibility" class="col-sm-12 action-button">
                                <a @click="printDocument('brief_of_evidence')" class="btn btn-primary btn-block">
                                <!--a @click="createProsecutionBrief" class="btn btn-primary btn-block"-->
                                  Print Brief of Evidence
                                </a>
                          </div>
                        </div>
                        <div  class="row">
                          <div v-if="canUserAction && briefOfEvidenceStatus" class="col-sm-12 action-button">
                                <a @click="addWorkflow('send_to_manager')" class="btn btn-primary btn-block">
                                <!--a @click="createProsecutionBrief" class="btn btn-primary btn-block"-->
                                  Send To Manager
                                </a>
                          </div>
                        </div>
                        <div  class="row">
                          <div v-if="backToOfficerVisibility" class="col-sm-12 action-button">
                                <a @click="addWorkflow('back_to_officer')" class="btn btn-primary btn-block">
                                <!--a @click="createProsecutionBrief" class="btn btn-primary btn-block"-->
                                  Back To Officer
                                </a>
                          </div>
                        </div>
                        <div class="row">
                          <div v-if="canUserAction && withManagerStatus" class="col-sm-12 action-button">
                                <a @click="addWorkflow('approve_brief_of_evidence')" class="btn btn-primary btn-block">
                                <!--a @click="createProsecutionBrief" class="btn btn-primary btn-block"-->
                                  Approve
                                </a>
                          </div>
                        </div>
                        <div class="row">
                          <div v-if="canUserAction && withProsecutionCoordinatorStatus" class="col-sm-12 action-button">
                                <a @click="addWorkflow('prosecution_brief')" class="btn btn-primary btn-block">
                                <!--a @click="createProsecutionBrief" class="btn btn-primary btn-block"-->
                                  Prosecution Brief
                                </a>
                          </div>
                        </div>
                        <div class="row">
                          <div v-if="canUserAction && withProsecutionCoordinatorProsecutionBriefStatus" class="col-sm-12 action-button">
                                <a @click="addWorkflow('send_to_prosecution_council')" class="btn btn-primary btn-block">
                                <!--a @click="createProsecutionBrief" class="btn btn-primary btn-block"-->
                                  Send To Prosecution Council
                                </a>
                          </div>
                        </div>
                        <div  class="row">
                          <div v-if="canUserAction && prosecutionBriefVisibility" class="col-sm-12 action-button">
                                <a @click="printDocument('prosecution_brief')" class="btn btn-primary btn-block">
                                <!--a @click="createProsecutionBrief" class="btn btn-primary btn-block"-->
                                  Print Prosecution Brief
                                </a>
                          </div>
                        </div>
                        <div class="row">
                          <div v-if="canUserAction && withProsecutionCouncilStatus" class="col-sm-12 action-button">
                                <a @click="addWorkflow('back_to_prosecution_coordinator')" class="btn btn-primary btn-block">
                                <!--a @click="createProsecutionBrief" class="btn btn-primary btn-block"-->
                                  Back to Prosecution Coordinator
                                </a>
                          </div>
                        </div>
                        <div class="row">
                          <div v-if="canUserAction && withProsecutionCouncilStatus" class="col-sm-12 action-button">
                                <a @click="addWorkflow('endorse_prosecution_brief')" class="btn btn-primary btn-block">
                                <!--a @click="createProsecutionBrief" class="btn btn-primary btn-block"-->
                                  Endorse Prosecution Brief
                                </a>
                          </div>
                        </div>
                        <div class="row">
                          <div v-if="canUserAction && withProsecutionManagerStatus" class="col-sm-12 action-button">
                                <a @click="addWorkflow('approve_for_court')" class="btn btn-primary btn-block">
                                <!--a @click="createProsecutionBrief" class="btn btn-primary btn-block"-->
                                  Approve for Court
                                </a>
                          </div>
                        </div>
                        <div class="row">
                          <div v-if="canUserAction && withProsecutionManagerStatus" class="col-sm-12 action-button">
                                <a @click="addWorkflow('back_to_prosecution_council')" class="btn btn-primary btn-block">
                                <!--a @click="createProsecutionBrief" class="btn btn-primary btn-block"-->
                                  Back to Prosecution Council
                                </a>
                          </div>
                        </div>

                        <div id="close-button" class="row">
                          <div v-if="canUserAction && !closedStatus" class="col-sm-12 action-button">
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
                    <ul class="nav nav-pills">
                        <li class="nav-item active"><a data-toggle="tab" :href="'#'+runTab">Running Sheet</a></li>
                        <li class="nav-item"><a data-toggle="tab" :href="'#'+cTab" >Case Details</a></li>
                        <li v-if="briefOfEvidenceVisibility" class="nav-item"><a data-toggle="tab" :href="'#'+bTab" >Brief of Evidence</a></li>
                        <li v-if="prosecutionBriefVisibility" class="nav-item"><a data-toggle="tab" :href="'#'+pTab" >Prosecution Brief</a></li>
                        <!--li v-if="withProsecutionCoordinatorCourtStatus" class="nav-item"><a data-toggle="tab" :href="'#'+cpTab" >Court Proceedings</a></li-->
                        <li v-if="courtProceedingsVisibility" class="nav-item"><a data-toggle="tab" :href="'#'+cpTab" >Court Proceedings</a></li>
                        <li class="nav-item"><a data-toggle="tab" :href="'#'+rTab">Related Items</a></li>
                        <!--li class="nav-item"><a data-toggle="tab" :href="'#'+gTab">Generated Documents</a></li-->
                    </ul>
                    <div class="tab-content">
                        <div :id="runTab" class="tab-pane fade in active">
                          <FormSection :formCollapse="false" label="Running Sheet" Index="0">
                            <div class="col-sm-12 form-group"><div class="row">
                                <div>
                                    <div class="row action-button">
                                        <!--div v-if="canUserAction" class="col-sm-12"-->
                                        <!--div class="col-sm-1 pull-right" /-->
                                        <div v-if="!readonlyRunningSheet">
                                              <a @click="createNewRunningSheetEntry()" class="btn btn-primary pull-right new-row-button" >
                                                New Row
                                              </a>
                                        </div>
                                        <div v-else>
                                              <a class="btn btn-primary pull-right new-row-button" disabled>
                                                New Row
                                              </a>
                                        </div>
                                    </div>
                                    <datatable
                                    ref="running_sheet_table"
                                    id="running-sheet-table"
                                    :dtOptions="dtOptionsRunningSheet"
                                    :dtHeaders="dtHeadersRunningSheet"
                                    parentStyle=" "
                                    />
                                </div>
                            </div></div>
                          </FormSection>
                        </div>
                        <div :id="cTab" class="tab-pane fade in">
                            <FormSection :formCollapse="false" label="Case Details">
                                <div class="col-sm-12 form-group"><div class="row">
                                    <label class="col-sm-10">Title
                                        <input :readonly="readonlyForm" type="text" class="form-control" v-model="legal_case.title" />
                                    </label>
                                </div></div>
                                <div class="col-sm-12 form-group"><div class="row">
                                    <label class="col-sm-10">Details
                                        <textarea :readonly="readonlyForm" class="form-control location_address_field" v-model="legal_case.details" />
                                    </label>
                                </div></div>
                                <div class="col-sm-12 form-group"><div class="row">
                                    <div v-if="legal_case.defaultDocumentUrl">
                                        <label class="col-sm-10">Documents
                                            <filefield
                                            ref="legal_case_documents"
                                            name="legal-case-documents"
                                            :isRepeatable="true"
                                            :documentActionUrl="legal_case.defaultDocumentUrl"
                                            :readonly="readonlyForm"
                                            />
                                        </label>
                                    </div>
                                </div></div>
                            </FormSection>
                        </div>
                        <div :id="bTab" class="tab-pane fade in">
                            <BriefOfEvidence
                            ref="brief_of_evidence"
                            :readonly="briefOfEvidenceReadonly"/>
                        </div>
                        <div :id="pTab" class="tab-pane fade in">
                            <ProsecutionBrief
                            ref="prosecution_brief"
                            :readonly="prosecutionBriefReadonly"/>
                        </div>
                        <div :id="cpTab" class="tab-pane fade in">
                            <CourtProceedings
                            v-if="legal_case.court_proceedings" />
                        </div>
                        <div :id="rTab" class="tab-pane fade in">
                            <FormSection :formCollapse="false" label="Related Items">
                                <div class="col-sm-12 form-group"><div class="row">
                                    <div class="col-sm-12" v-if="relatedItemsVisibility">
                                        <RelatedItems
                                        v-bind:key="relatedItemsBindId"
                                        :parent_update_related_items="setRelatedItems"
                                        :readonlyForm="readonlyForm"
                                        parentComponentName="legal_case"
                                        />
                                    </div>
                                </div></div>
                            </FormSection>
                        </div>
                        <!--div :id="gTab" class="tab-pane fade in">
                            <FormSection :formCollapse="false" label="Generated Documents">
                                <div class="col-sm-12 form-group"><div class="row">
                                    <div v-if="legal_case.generatedDocumentsUrl">
                                        <filefield
                                        ref="generated_documents"
                                        name="generated-documents"
                                        :isRepeatable="true"
                                        :readonly="true"
                                        :documentActionUrl="legal_case.generatedDocumentsUrl"
                                        />
                                    </div>
                                </div></div>
                            </FormSection>
                        </div-->
                    </div>
                </div>
            </div>
          </div>

        <div v-if="canUserAction" class="navbar navbar-fixed-bottom" style="background-color: #f5f5f5 ">
            <div class="navbar-inner">
                <div class="container">
                    <p class="pull-right" style="margin-top:5px;">
                        <button v-if="showSpinner && showExit" disabled type="button" @click.prevent="save('exit')" class="btn btn-primary">
                            <i class="fa fa-spinner fa-spin"/> Saving</button>
                        <button v-else type="button" @click.prevent="saveExit()" class="btn btn-primary" >Save and Exit</button>
                        <button v-if="showSpinner && !showExit" disabled type="button" @click.prevent="save('noexit')" class="btn btn-primary" >
                            <i class="fa fa-spinner fa-spin"/> Saving</button>
                        <button v-else type="button" @click.prevent="save()" class="btn btn-primary">Save and Continue</button>
                    </p>
                </div>
            </div>
        </div>
        <div v-if="offenceInitialised">
            <Offence
            ref="offence"
            :parent_update_function="loadLegalCase"
            :region_id="legal_case.region_id"
            :district_id="legal_case.district_id"
            :allocated_group_id="legal_case.allocated_group_id"
            v-bind:key="offenceBindId"
            />
        </div>
        <div v-if="sanctionOutcomeInitialised">
            <SanctionOutcome
            ref="sanction_outcome"
            :parent_update_function="loadLegalCase"
            v-bind:key="sanctionOutcomeBindId"
            />
        </div>
        <div v-if="inspectionInitialised">
            <Inspection
            ref="inspection"
            :parent_update_function="loadLegalCase"
            v-bind:key="inspectionBindId"
            />
        </div>
        <Magic ref="magic" />
        <div v-if="personOrArtifactInitialised">
            <PersonOrArtifactModal
            ref="person_or_artifact_modal"
            :readonlyForm="readonlyForm"
            v-bind:key="personOrArtifactBindId"
            @modal-action="receivePersonOrArtifactEntity"
            :rowNumberSelected="rowNumberSelected"
            :initialTabSelected="tabSelected"
            :entityEdit="entityEdit"
            />
        </div>
        <div v-if="runningSheetHistoryEntryBindId">
            <RunningSheetHistory
            ref="running_sheet_history"
            :runningSheetHistoryEntryInstance="runningSheetHistoryEntryInstance"
            v-bind:key="runningSheetHistoryEntryBindId"
            />
        </div>
        <div v-if="legalCaseWorkflowBindId">
            <LegalCaseWorkflow
            ref="legal_case_workflow"
            :workflow_type="workflow_type"
            v-bind:key="legalCaseWorkflowBindId"
            />
        </div>
        <div v-if="generateDocumentBindId">
            <GenerateDocument
            ref="generate_document"
            :document_type="documentTypeToGenerate"
            v-bind:key="generateDocumentBindId"
            />
        </div>
    </div>
</template>
<script>
import Vue from "vue";
import FormSection from "@/components/forms/section_toggle.vue";
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
import Inspection from '../inspection/create_inspection_modal';
import filefield from '@/components/common/compliance_file.vue';
import RelatedItems from "@common-components/related_items.vue";
require("select2/dist/css/select2.min.css");
require("select2-bootstrap-theme/dist/select2-bootstrap.min.css");
import hash from 'object-hash';
import Magic from './magic';
//import SearchPersonOrganisationModal from '@/components/common/search_person_or_organisation_modal';
import PersonOrArtifactModal from '@/components/common/person_or_artifact_modal';
import _ from 'lodash';
import RunningSheetHistory from './running_sheet_history'
import LegalCaseWorkflow from './legal_case_workflow'
//import TreeSelect from "@/components/compliance_forms/treeview.vue";
import TreeSelect from '@riophae/vue-treeselect'
import '@riophae/vue-treeselect/dist/vue-treeselect.css'
import BriefOfEvidence from './brief_of_evidence';
import ProsecutionBrief from './prosecution_brief';
import CourtProceedings from './court_proceedings';
import GenerateDocument from './generate_document';


export default {
    name: "ViewLegalCase",
    data: function() {
        return {
            //boeRoiTicked: [],
            //boeRoiOptions: [],
            //boeOtherStatementsOptions: [],
            documentTypeToGenerate: '',
            entityEdit: {},
            uuid: 0,
            showSpinner: false,
            showExit: false,
            rowNumberSelected: '',
            tabSelected: '',
            runningSheetUrl: [],
            runningSheetEntriesUpdated: [],
            runningSheetHistoryEntryBindId: '',
            legalCaseWorkflowBindId: '',
            generateDocumentBindId: '',
            runningSheetHistoryEntryInstance: '',
            //runningSheetArtifactList: [],
            //runningSheetPersonList: [],
            objectHash: null,
            runTab: 'runTab'+this._uid,
            rTab: 'rTab'+this._uid,
            //gTab: 'gTab'+this._uid,
            cTab: 'cTab'+this._uid,
            cpTab: 'cpTab'+this._uid,
            bTab: 'bTab'+this._uid,
            pTab: 'pTab'+this._uid,
            current_schema: [],
            //workflowBindId: '',
            workflow_type: '',
            comms_url: helpers.add_endpoint_json(
              api_endpoints.legal_case,
              this.$route.params.legal_case_id + "/comms_log"
            ),
            comms_add_url: helpers.add_endpoint_json(
              api_endpoints.legal_case,
              this.$route.params.legal_case_id + "/add_comms_log"
            ),
            logs_url: helpers.add_endpoint_json(
              api_endpoints.legal_case,
              this.$route.params.legal_case_id + "/action_log"
            ),
            assign_url: helpers.add_endpoint_join(
                api_endpoints.legal_case,
                this.$route.params.legal_case_id + '/update_assigned_to_id/'
            ),
            assignmentKey: 0,
            sanctionOutcomeInitialised: false,
            personOrArtifactInitialised: false,
            //searchPersonOrganisationKeyPosition: null,
            offenceInitialised: false,
            inspectionInitialised: false,
            hashAttributeWhitelist: [
              'allocated_group_id',
              'case_created_date',
              'case_created_time',
              'details',
              'title',
              'legal_case_priority_id',
              'region_id',
              'district_id',
            ],
            searchPersonKeyPressed: false,
            searchArtifactKeyPressed: false,
            insertUrlKeyPressed: false,
            //magicValue: null,
            magic: true,
            dtHeadersRunningSheet: [
                "id",
                "Number",
                "Date",
                "Time",
                "User",
                "Description",
                "deleted",
                "Action",
            ],
            dtOptionsRunningSheet: {
                order: [
                    [0, 'desc'],
                    ],
                columns: [
                    {
                        data: 'id',
                        visible: false,
                        mRender: function(data, type, row) {
                            return row.id;
                        }
                    },
                    {
                        data: 'id',
                        mRender: function(data, type, row) {
                            let retStr = row.number;
                            return retStr;
                        }
                    },
                    {
                        data: 'id',
                        mRender: function(data, type, row) {
                            let retStr = row.date_mod;
                            return retStr;
                        }
                    },
                    {
                        data: 'id',
                        mRender: function(data, type, row) {
                            let retStr = row.time_mod;
                            return retStr;
                        }
                    },
                    {
                        data: 'id',
                        mRender: function(data, type, row) {
                            let retStr = row.user_full_name;
                            return retStr;
                        }
                    },
                    {
                        data: 'id',
                        mRender: function(data, type, row) {
                            let retStr = '';
                            retStr = `<div id=${row.number} style="min-height:20px" contenteditable="true">${row.description}</div>`
                            if (row.deleted) {
                                retStr = '<strike>' +
                                    `<div id=${row.number} style="min-height:20px" contenteditable="false">${row.description}</div>`
                                    '</strike>';
                            } else if (!row.action) {
                                retStr = `<div id=${row.number} style="min-height:20px" contenteditable="false">${row.description}</div>`
                            }
                            return retStr;
                        }
                    },
                    {
                        data: 'id',
                        visible: false,
                        mRender: function(data, type, row) {
                            return row.deleted;
                        }
                    },
                    {
                        data: 'id',
                        mRender: function(data, type, row) {
                            let retStr = '';
                            let rowIdDel = row.number.replace('-', 'D')
                            let rowIdHist = row.number.replace('-', 'H')
                            let rowIdReinstate = row.number.replace('-', 'R')
                            retStr += `<a id=${rowIdHist} class="row_history" href="#">History</a><br/><br/>`
                            if (row.action) {
                                //retStr += `<a id=${rowIdHist} class="row_history" href="#">History</a><br/><br/>`
                                if (!row.deleted) {
                                    retStr += `<a id=${rowIdDel} class="row_delete" href="#">Delete</a><br/>`
                                } else {
                                    retStr += `<a id=${rowIdReinstate} class="row_reinstate" href="#">Reinstate</a><br/>`
                                }

                            }
                            return retStr;

                        }
                    },
                ]
            }
      };
  },
  components: {
    CommsLogs,
    FormSection,
    datatable,
    Offence,
    SanctionOutcome,
    filefield,
    RelatedItems,
    Inspection,
    Magic,
    PersonOrArtifactModal,
    RunningSheetHistory,
    LegalCaseWorkflow,
    TreeSelect,
    BriefOfEvidence,
    CourtProceedings,
    ProsecutionBrief,
    GenerateDocument,
    Assignment,
  },
  computed: {
    ...mapGetters('legalCaseStore', {
      legal_case: "legal_case",
    }),
    ...mapGetters({
        current_user: 'current_user'
    }),
    csrf_token: function() {
      return helpers.getCookie("csrftoken");
    },
    statusDisplay: function() {
        return this.legal_case.status ? this.legal_case.status.name : '';
    },
    statusId: function() {
        return this.legal_case.status ? this.legal_case.status.id : '';
    },
    readonlyForm: function() {
        let readonly = true
        if (this.legal_case && this.legal_case.id && !this.closedStatus) {
            readonly = !this.legal_case.can_user_action;
        }
        return readonly
    },
    readonlyRunningSheet: function() {
        let readonly = true
        if (this.legal_case && this.legal_case.id && this.legal_case.can_user_action && this.openStatus) {
            readonly = false;
        }
        return readonly
    },
    backToOfficerVisibility: function() {
        let visibility = false;
        if (this.canUserAction && (
            this.withProsecutionCoordinatorStatus ||
            this.withProsecutionCoordinatorProsecutionBriefStatus ||
            this.withManagerStatus)
            //this.withProsecutionCouncilStatus)
        ) {
            visibility = true;
        }
        return visibility;
    },
    closedStatus: function() {
        let returnStatus = false
        if (this.legal_case && this.statusId === 'closed') {
            returnStatus = true
        }
        return returnStatus
    },
    withProsecutionCoordinatorCourtStatus: function() {
        let returnStatus = false
        if (this.legal_case && this.statusId === 'with_prosecution_coordinator_court') {
            returnStatus = true
        }
        return returnStatus
    },
    withProsecutionManagerStatus: function() {
        let returnStatus = false
        if (this.legal_case && this.statusId === 'with_prosecution_manager') {
            returnStatus = true
        }
        return returnStatus
    },
    withProsecutionCouncilStatus: function() {
        let returnStatus = false
        if (this.legal_case && this.statusId === 'with_prosecution_council') {
            returnStatus = true
        }
        return returnStatus
    },
    withProsecutionCoordinatorProsecutionBriefStatus: function() {
        let returnStatus = false
        if (this.legal_case && this.statusId === 'with_prosecution_coordinator_prosecution_brief') {
            returnStatus = true
        }
        return returnStatus
    },
    withProsecutionCoordinatorStatus: function() {
        let returnStatus = false
        if (this.legal_case && this.statusId === 'with_prosecution_coordinator') {
            returnStatus = true
        }
        return returnStatus
    },
    withManagerStatus: function() {
        let returnStatus = false
        if (this.legal_case && this.statusId === 'with_manager') {
            returnStatus = true
        }
        return returnStatus
    },
    briefOfEvidenceStatus: function() {
        let returnStatus = false
        if (this.legal_case && this.statusId === 'brief_of_evidence') {
            returnStatus = true
        }
        return returnStatus
    },
    prosecutionBriefStatus: function() {
        let returnStatus = false
        if (this.legal_case && this.statusId === 'prosecution_brief') {
            returnStatus = true
        }
        return returnStatus
    },
    openStatus: function() {
        let returnStatus = false
        if (this.legal_case && this.statusId === 'open') {
            returnStatus = true
        }
        return returnStatus
    },
    runningSheetTabListClass: function() {
        let tabClass = 'nav-item';
        if (this.openStatus) {
            tabClass += ' active';
        }
        return tabClass;
    },
    briefOfEvidenceTabListClass: function() {
        let tabClass = 'nav-item';
        if (this.briefOfEvidenceStatus) {
            tabClass += ' active';
        }
        return tabClass;
    },
    prosecutionBriefTabListClass: function() {
        let tabClass = 'nav-item';
        if (this.prosecutionBriefStatus) {
            tabClass += ' active';
        }
        return tabClass;
    },
    runningSheetTabClass: function() {
        let tabClass = 'tab-pane fade in';
        if (this.openStatus) {
            tabClass += ' active';
        }
        return tabClass;
    },
    briefOfEvidenceTabClass: function() {
        let tabClass = 'tab-pane fade in';
        if (this.briefOfEvidenceStatus) {
            tabClass += ' active';
        }
        return tabClass;
    },
    prosecutionBriefTabClass: function() {
        let tabClass = 'tab-pane fade in';
        if (this.prosecutionBriefStatus) {
            tabClass += ' active';
        }
        return tabClass;
    },
    readonlyBriefOfEvidence: function() {
        let readonly = true
        if (this.legal_case && this.legal_case.id) {
            readonly = !this.legal_case.can_user_action;
        }
        return readonly
    },
    canUserAction: function() {
        let return_val = false
        if (this.legal_case && this.legal_case.id) {
            return_val = this.legal_case.can_user_action;
        }
        return return_val
    },
    offenceExists: function() {
        for (let item of this.legal_case.related_items) {
            if (item.model_name.toLowerCase() === 'offence') {
                return true
            }
        }
        // return false if no related item is an Offence
        return false
    },
    sanctionOutcomeVisibility: function() {
        let sanction_outcome_visibility = false;
        if (this.legal_case.status && this.offenceExists && this.legal_case.can_user_action) {
            sanction_outcome_visibility = this.legal_case.status.id === 'open' ? true : false;
        }
        return sanction_outcome_visibility;
    },
    relatedItemsBindId: function() {
        let timeNow = Date.now()
        let bindId = null;
        if (this.legal_case && this.legal_case.id) {
            bindId = 'legal_case_' + this.legal_case.id + '_' + this.uuid;
        } else {
            bindId = timeNow.toString();
        }
        return bindId;
    },
    relatedItemsVisibility: function() {
        let related_items_visibility = false;
        if (this.legal_case && this.legal_case.id) {
            related_items_visibility = true;
        }
        return related_items_visibility;
    },
    personOrArtifactBindId: function() {
        let person_or_artifact_id = ''
        person_or_artifact_id = this.tabSelected + parseInt(this.uuid);
        return person_or_artifact_id;
    },
    offenceBindId: function() {
        let offence_bind_id = ''
        offence_bind_id = 'offence' + parseInt(this.uuid);
        return offence_bind_id;
    },
    briefOfEvidenceVisibility: function() {
        let visible = false;
        if (this.legal_case &&
            this.legal_case.id &&
            this.legal_case.brief_of_evidence &&
            !this.openStatus
        )
        {
            visible = true;
        }
        return visible;
    },
    briefOfEvidenceReadonly: function() {
        let readonly = true;
        if (this.briefOfEvidenceStatus) {
            readonly = false;
        }
        return readonly;
    },
    prosecutionBriefReadonly: function() {
        let readonly = true;
        if (this.withProsecutionCoordinatorProsecutionBriefStatus) {
            readonly = false;
        }
        return readonly;
    },
    prosecutionBriefVisibility: function() {
        let visible = false;
        if (this.legal_case &&
            this.legal_case.id &&
            this.legal_case.brief_of_evidence &&
            this.legal_case.prosecution_brief &&
            // following status values are excluded
            !([
                'open',
                'brief_of_evidence',
                'with_manager',
                'with_prosecution_coordinator',
            ].includes(this.statusId))
        )
        {
            visible = true;
        }
        return visible;
    },
    courtProceedingsVisibility: function() {
        let visible = false;
        if (this.legal_case &&
            this.legal_case.id &&
            this.legal_case.brief_of_evidence &&
            this.legal_case.prosecution_brief &&
            this.legal_case.court_proceedings &&
            // following status values are included
            [
                'with_prosecution_coordinator_court',
                'closed',
                //'with_prosecution_council',
                //'with_prosecution_manager',
            ].includes(this.statusId)
        )
        {
            visible = true;
        }
        return visible;
    },
    sanctionOutcomeBindId: function() {
        let sanction_outcome_bind_id = ''
        sanction_outcome_bind_id = 'sanction_outcome' + parseInt(this.uuid);
        return sanction_outcome_bind_id;
    },
    inspectionBindId: function() {
        let inspection_bind_id = ''
        inspection_bind_id = 'inspection' + parseInt(this.uuid);
        return inspection_bind_id;
    },
    tabSelectedKeyCombination: function() {
        let keyCombination = '';
        if (this.tabSelected === 'person') {
            keyCombination = '@@';
        } else if (this.tabSelected === 'artifact') {
            keyCombination = '!!';
        } else if (this.tabSelected === 'url') {
            keyCombination = '^^';
        }
        return keyCombination;
    },
  },
  filters: {
    formatDate: function(data) {
      return data ? moment(data).format("DD/MM/YYYY HH:mm:ss") : "";
    }
  },
  methods: {
    ...mapActions('legalCaseStore', {
      loadLegalCase: 'loadLegalCase',
      loadLegalCaseNoRunningSheet: 'loadLegalCaseNoRunningSheet',
      saveLegalCase: 'saveLegalCase',
      setLegalCase: 'setLegalCase',
      setRelatedItems: 'setRelatedItems',
      setRunningSheetEntries: 'setRunningSheetEntries',
      setRunningSheetEntryDescription: 'setRunningSheetEntryDescription',
      setRunningSheetTransform: 'setRunningSheetTransform',
      setAddRunningSheetEntry: 'setAddRunningSheetEntry',
      setRunningSheetEntry: 'setRunningSheetEntry',
      addToRunningSheetPersonList: 'addToRunningSheetPersonList',
      setBriefOfEvidence: 'setBriefOfEvidence',
      setProsecutionBrief: 'setProsecutionBrief',
    }),
    ...mapActions({
        loadCurrentUser: 'loadCurrentUser',
    }),
    setRunningSheetHistoryEntryBindId: function() {
        if (this.runningSheetHistoryEntryInstance) {
            this.uuid += 1;
            this.runningSheetHistoryEntryBindId = this.runningSheetHistoryEntryInstance + '_' + this.uuid;
        }
    },
    setLegalCaseWorkflowBindId: function() {
        this.uuid += 1;
        this.legalCaseWorkflowBindId = 'legal_case_workflow_' + this.uuid;
    },
    setGenerateDocumentBindId: function() {
        this.uuid += 1;
        this.generateDocumentBindId = 'generate_document_' + this.uuid;
    },

    runningSheetTransformWrapper: async function() {
        let runningSheet = []
        let i = 0;
        for (let r of this.runningSheetUrl) {
            if (this.runningSheetEntriesUpdated.includes(r.number)) {
                r.description = this.htmlToToken(r.description)
                r.user_id = this.current_user.id;
                runningSheet.push(r);
            }
            i += 1;
        }
        await this.setRunningSheetTransform(runningSheet)
    },
    receivePersonOrArtifactEntity: function({
        "row_number_selected": row_number_selected,
        "entity": entity,
        "action": action
    }) {
        // destroy modal
        this.personOrArtifactInitialised = false;
        console.log(row_number_selected);
        console.log(entity);
        console.log(action);
        let recordNumber = row_number_selected;
        let recordNumberElement = $('#' + recordNumber)
        let recordDescriptionHtml = ''
        if (action === 'cancel') {
            recordDescriptionHtml = this.cancelModalUrl(recordNumberElement)
        } else if (entity && entity.data_type === 'individual' && action === 'ok') {
            recordDescriptionHtml = this.insertPersonModalUrl({"entity": entity, "recordNumberElement": recordNumberElement})
        } else if (entity && entity.artifact_type && action === 'ok') {
            recordDescriptionHtml = this.insertArtifactModalUrl({"entity": entity, "recordNumberElement": recordNumberElement})
        } else if (entity && entity.data_type === 'url' && action === 'ok') {
            recordDescriptionHtml = this.insertModalUrl({"entity": entity, "recordNumberElement": recordNumberElement})
        }
        if (recordNumber) {
            this.updateRunningSheetUrlEntry({
                "recordNumber": recordNumber,
                "recordDescription": recordDescriptionHtml,
                "redraw": true,
            })
        }
    },
    insertPersonModalUrl: function({"entity": entity, "recordNumberElement": recordNumberElement}) {
        console.log(entity);
        console.log(recordNumberElement);
        let replacementVal = ''
        let urlId = entity.data_type + "-" + entity.id;
        if (entity.full_name) {
            //replacementVal = `<a contenteditable="false" id="${urlId}" class="entity_edit" target="_blank" href="/internal/users/${entity.id}">${entity.full_name}</a>`;
            replacementVal = `<span contenteditable="false" id="${urlId}" class="entity_edit">${entity.full_name}</span>`;
            // add to runningSheetPersonList
            this.addToRunningSheetPersonList(entity)
            //this.legal_case.runningSheetPersonList.push(entity)
        }
        //let recordDescriptionHtml = recordNumberElement[0].innerHTML.replace(this.tabSelectedKeyCombination, replacementVal).replace(/&nbsp\;/g, ' ');
        let recordDescriptionHtml = recordNumberElement[0].innerHTML.replace(this.tabSelectedKeyCombination, replacementVal);
        return recordDescriptionHtml;
    },
    insertArtifactModalUrl: function({"entity": entity, "recordNumberElement": recordNumberElement}) {
        console.log(entity)
        let replacementVal = '';
        let urlDescription = entity.identifier ? entity.identifier : entity.display;
        let urlId = entity.data_type + "-" + entity.id;

        if (urlDescription) {
            //replacementVal = `<a contenteditable="false" id="${urlId}" class="entity_edit" target="_blank" href="/internal/object/${entity.id}">${urlDescription}</a>`;
            replacementVal = `<span contenteditable="false" id="${urlId}" class="entity_edit">${urlDescription}</span>`;
            // add to runningSheetArtifactList
            /*
            if (this.legal_case && !this.legal_case.runningSheetArtifactList) {
                this.legal_case.runningSheetArtifactList = []
            }
            this.legal_case.runningSheetArtifactList.push(entity)
            */
        }
        //let recordDescriptionHtml = recordNumberElement[0].innerHTML.replace(this.tabSelectedKeyCombination, replacementVal).replace(/&nbsp\;/g, ' ');
        let recordDescriptionHtml = recordNumberElement[0].innerHTML.replace(this.tabSelectedKeyCombination, replacementVal);
        console.log(recordDescriptionHtml);
        return recordDescriptionHtml;
    },
    cancelModalUrl: function(recordNumberElement) {
        console.log(recordNumberElement)
        let replacementVal = ''
        //let recordDescriptionHtml = recordNumberElement[0].innerHTML.replace(this.tabSelectedKeyCombination, replacementVal).replace(/&nbsp\;/g, ' ');
        let recordDescriptionHtml = recordNumberElement[0].innerHTML.replace(this.tabSelectedKeyCombination, replacementVal);
        return recordDescriptionHtml;
    },
    insertModalUrl: function({"entity": entity, "recordNumberElement": recordNumberElement}) {
        console.log(entity)
        let replacementVal = ''
        /*
        console.log(entity)
        console.log(recordNumberElement)
        */

        if (entity.url) {
            //let fullUrl = "https://" + entity.url.trim();
            let fullUrl = entity.urlProtocol + "://" + entity.url.trim();
            replacementVal = `<a contenteditable="false" target="_blank" href=${fullUrl}>${entity.url}</a>`
            //replacementVal = `<a target="_blank" href=${fullUrl}>${entity.url}</a>`
        }
        //let recordDescriptionHtml = recordNumberElement[0].innerHTML.replace(this.tabSelectedKeyCombination, replacementVal).replace(/&nbsp\;/g, ' ');
        let recordDescriptionHtml = recordNumberElement[0].innerHTML.replace(this.tabSelectedKeyCombination, replacementVal);
        //console.log(recordDescriptionHtml)
        return recordDescriptionHtml;
    },
    constructRunningSheetTable: function(pk){
        console.log("constructRunningSheetTable")
        if (!pk) {
            this.$refs.running_sheet_table.vmDataTable.clear().draw();
        }
        //let actionColumn = !this.readonlyForm;
        let actionColumn = !this.readonlyRunningSheet;
        if (this.runningSheetUrl){
            for(let i = 0;i < this.runningSheetUrl.length; i++){
                if (!pk || this.runningSheetUrl[i].id === pk) {
                    this.$refs.running_sheet_table.vmDataTable.row.add({
                        "id": this.runningSheetUrl[i].id,
                        "number": this.runningSheetUrl[i].number,
                        "date_mod": this.runningSheetUrl[i].date_mod,
                        "time_mod": this.runningSheetUrl[i].time_mod,
                        "user_full_name": this.runningSheetUrl[i].user_full_name,
                        "description": this.runningSheetUrl[i].description,
                        "deleted": this.runningSheetUrl[i].deleted,
                        "action": actionColumn,
                    }).draw();
                }
            }
        }
        console.log("constructRunningSheetTable - end")
    },
    constructRunningSheetTableEntry: function( rowNumber ){
        console.log('rowNumber')
        console.log(rowNumber)

        let actionColumn = !this.readonlyForm;
        if (this.$refs.running_sheet_table && this.$refs.running_sheet_table.vmDataTable) {
            console.log("constructRunningSheetTableEntry");
            this.$refs.running_sheet_table.vmDataTable.rows().every((rowIdx, tableLoop, rowLoop) => {
                let rowData = this.$refs.running_sheet_table.vmDataTable.row(rowIdx).data()
                /*
                console.log(rowIdx)
                console.log(rowData)
                */
                if (rowData.number === rowNumber) {
                    let i = 0;
                    for (let r of this.runningSheetUrl) {
                        if (r.number === rowNumber) {
                            rowData.date_mod = this.runningSheetUrl[rowIdx].date_mod;
                            rowData.time_mod = this.runningSheetUrl[rowIdx].time_mod;
                            rowData.user_full_name = this.runningSheetUrl[rowIdx].user_full_name;
                            rowData.description = this.runningSheetUrl[rowIdx].description;
                            rowData.deleted = this.runningSheetUrl[rowIdx].deleted;
                            rowData.action = actionColumn;
                            this.$refs.running_sheet_table.vmDataTable.row(rowIdx).invalidate().draw();
                        }
                        i += 1;
                    }
                }
            });
        }
    },
    createNewRunningSheetEntry: async function() {
        // save changes to running sheet
        //await this.save({ "createNewRow": true})

        // add new entry and add to datatable
        let payload = {
            "legal_case_id": this.legal_case.id,
            "user_id": this.current_user.id,
        }
        let fetchUrl = helpers.add_endpoint_join(
            api_endpoints.legal_case,
            this.legal_case.id + '/create_running_sheet_entry/'
            )
        let updatedRunningSheet = await Vue.http.post(fetchUrl, payload);
        console.log(updatedRunningSheet)
        if (updatedRunningSheet.ok) {
            await this.setAddRunningSheetEntry(updatedRunningSheet.body);
            let returnPayload = _.cloneDeep(updatedRunningSheet.body);
            returnPayload.description = this.tokenToHtml(returnPayload.description);
            this.runningSheetUrl.push(returnPayload);
            this.constructRunningSheetTable(returnPayload.id);
        }

    },
    openInspection() {
      this.uuid += 1;
      this.inspectionInitialised = true;
        this.$nextTick(async () => {
          //await this.saveLegalCase({create: false, internal: true })
          await this.save({internalFlag:true});
          this.$refs.inspection.isModalOpen = true
      });
    },

    openSanctionOutcome(){
      this.uuid += 1;
      this.sanctionOutcomeInitialised = true;
      this.$nextTick(async () => {
          //await this.saveLegalCase({create: false, internal: true })
          await this.save({internalFlag:true});
          this.$refs.sanction_outcome.isModalOpen = true;
      });
    },
    openOffence(){
      this.uuid += 1;
      this.offenceInitialised = true;
      this.$nextTick(async () => {
          //await this.saveLegalCase({create: false, internal: true })
          await this.save({internalFlag:true});
          this.$refs.offence.isModalOpen = true;
      });
    },
    //openPersonOrObject(rowNumber){
    openPersonOrArtifact(){
      this.uuid += 1;
      //this.rowNumberSelected = rowNumber;
      this.personOrArtifactInitialised = true;
      //this.personObjectKeyPosition = offset;
      this.$nextTick(async () => {
          //await this.save({internalFlag:true, noRunningSheet:true});
          await this.loadLegalCaseNoRunningSheet({legal_case_id: this.legal_case.id});
          this.$refs.person_or_artifact_modal.isModalOpen = true;
      });
    },
    addWorkflow: function(workflow_type) {
        console.log(workflow_type)
        /*
        if (['brief_of_evidence', 'prosecution_brief'].includes(workflow_type)) {
            // Save legal_case first
            await this.save({
                "create": false,
                "internal": true
            })
            // workflow_action api method
            //let post_url = '/api/legal_case/' + this.legal_case.id + '/workflow_action/'
            let postUrl = helpers.add_endpoint_join(
                api_endpoints.legal_case,
                this.legal_case.id + '/workflow_action/'
            );
            let payload = new FormData();
            workflow_type ? payload.append('workflow_type', workflow_type) : null;
            let res = await Vue.http.post(postUrl, payload);

        } else {
            // open workflow modal
            this.workflow_type = workflow_type;
            this.updateWorkflowBindId();
            this.$nextTick(() => {
                this.$refs.legal_case_workflow.isModalOpen = true;
            });
        }
        */
        // open workflow modal
        this.workflow_type = workflow_type;
        this.setLegalCaseWorkflowBindId();
        //this.updateWorkflowBindId();
        this.$nextTick(async () => {
            //await this.saveLegalCase({create: false, internal: true })
            await this.save({internalFlag:true});
            this.$refs.legal_case_workflow.isModalOpen = true;
        });
    },
    printDocument: function(documentType) {
        this.documentTypeToGenerate = documentType
        this.setGenerateDocumentBindId();
        this.$nextTick(async () => {
            //await this.saveLegalCase({create: false, internal: true })
            await this.save({internalFlag:true});
            this.$refs.generate_document.isModalOpen = true;
        });
    },

    saveExit: async function() {
        await this.save({ "returnToDash": true })
    },
    save: async function({
        returnToDash=false,
        createBriefOfEvidence=false,
        createProsecutionBrief=false,
        fullHttpResponse=false,
        //noRunningSheet=false,
        internalFlag=false,
    } = {}) {
      this.showSpinner = true;
      if (returnToDash) {
          this.showExit = true;
      }
      // prepare running sheet for save
      await this.runningSheetTransformWrapper();
      // add brief_of_evidence to legal_case
      if (this.$refs.brief_of_evidence) {
          await this.setBriefOfEvidence(this.$refs.brief_of_evidence.briefOfEvidence);
      }
      // add prosecution_brief to legal_case
      if (this.$refs.prosecution_brief) {
          await this.setProsecutionBrief(this.$refs.prosecution_brief.prosecutionBrief);
      }
        /*
      if (createNewRow) {
          //await this.saveLegalCase({ create: false, internal: true, createNewRow: true });
          await this.saveLegalCase({ internal: true, createNewRow: true });
          */
      await this.saveLegalCase({
          internal: internalFlag,
          createBriefOfEvidence: createBriefOfEvidence,
          createProsecutionBrief: createProsecutionBrief,
          fullHttpResponse: fullHttpResponse,
          //noRunningSheet: noRunningSheet,
      });
      if (returnToDash) {
        // remove redundant eventListeners
        window.removeEventListener('beforeunload', this.leaving);
        window.removeEventListener('onblur', this.leaving);
        // return to dash
        this.$router.push({ name: 'internal-legal-case-dash' });
      } else {
          this.calculateHash();
          this.runningSheetEntriesUpdated = [];
          //this.constructRunningSheetTableWrapper();
      }
      this.showSpinner = false;
      this.showExit = false;
    },
    magicMethod: function() {
        console.log("magic method");
        this.$refs.magic.isModalOpen = true;
        this.magic = false;
    },
    updateRunningSheetUrlEntry: function({
          recordNumber,
          recordDescription,
          redraw
    }) {
        console.log("updateRunningSheetUrl")
        if (this.magic && recordDescription && recordDescription.toLowerCase().includes('shibaken')) {
            this.magicMethod()
        }
        /*
        console.log(recordNumber)
        console.log(recordDescription)
        console.log(redraw)
        */
        let i = 0;
        for (let r of this.runningSheetUrl) {
            //console.log(r.deleted)
            if (r.number === recordNumber) {
                r.description = recordDescription
                /*
                if (recordDescription) {
                    r.description = recordDescription
                }
                */
                if (redraw) {
                    this.constructRunningSheetTableEntry( recordNumber );
                }
            }
            i += 1;
        }
    },
    runningSheetKeyup: function(e) {
        let rowObj = {}
        let recordNumber = e.target.id
        let recordDescriptionText = e.target.textContent
        let recordDescriptionHtml = e.target.innerHTML.replace(/\&nbsp\;/g, ' ');
        // add recordNumber to runningSheetEntriesUpdated
        if (!this.runningSheetEntriesUpdated.includes(recordNumber)) {
            this.runningSheetEntriesUpdated.push(recordNumber);
        }

        //const ignoreArray = [49, 50, 16]
        const ignoreArray = []
        if (ignoreArray.includes(e.which)) {
            //pass
        } else {
            for (let r of this.runningSheetUrl) {
                if (r.number === recordNumber) {
                    this.updateRunningSheetUrlEntry({
                        "recordNumber": recordNumber,
                        "recordDescription": recordDescriptionHtml,
                        "redraw": false
                    })
                    //this.searchPersonKeyPressed = false;
                    //this.searchObjectKeyPressed = false;
                }
            }
        }
    },
    runningSheetKeydown: async function(e) {
        console.log(e)
        if (e.key === '!' && e.shiftKey && this.searchArtifactKeyPressed) {
            // ensure entityEdit is empty
            this.entityEdit = {};
            this.rowNumberSelected = e.target.id;
            this.tabSelected = 'artifact';
            this.openPersonOrArtifact();
            //this.openInspection()
            this.searchArtifactKeyPressed = false;
        } else if (e.key === '!' && e.shiftKey) {
            this.searchArtifactKeyPressed = true;
            this.searchPersonKeyPressed = false;
            this.insertUrlKeyPressed = false;
        } else if (e.key === '@' && e.shiftKey && this.searchPersonKeyPressed) {
            //let rowElement = $('#' + e.target.id);
            //this.openSearchPersonOrganisation(e.target.id)
            this.entityEdit = {};
            this.rowNumberSelected = e.target.id;
            this.tabSelected = 'person';
            this.openPersonOrArtifact();
            this.searchPersonKeyPressed = false;
        } else if (e.key === '@' && e.shiftKey) {
            this.searchPersonKeyPressed = true;
            this.searchArtifactKeyPressed = false;
            this.insertUrlKeyPressed = false;
        } else if (e.key === '^' && e.shiftKey && this.insertUrlKeyPressed) {
            this.rowNumberSelected = e.target.id;
            this.tabSelected = 'url';
            //let rowElement = $('#' + e.target.id);
            this.openPersonOrArtifact();
            //console.log("open url")
            //this.openSearchPersonOrganisation(e.target.id);
            this.insertUrlKeyPressed = false;
        } else if (e.key === '^' && e.shiftKey) {
            this.insertUrlKeyPressed = true;
            this.searchPersonKeyPressed = false;
            this.searchArtifactKeyPressed = false;
        } else if (e.key === 'Shift' && e.shiftKey) {
            // pass
        } else {
            this.searchPersonKeyPressed = false;
            this.searchArtifactKeyPressed = false;
            this.insertUrlKeyPressed = false;
        }
    },
    htmlToToken: function(description) {
        let parsedText = description;
        // person transform
        //const personUrlRegex = /<a contenteditable\=\"false\" target\=\"\_blank\" href\=\"\/internal\/users\/\d+\"\>\w+(\s\w+)*\<\/a\>/g
        const personUrlRegex = /<span contenteditable\=\"false\" id=\"individual-\d+\"\ class=\"entity_edit\">\w+(\s\w+)*\<\/span\>/g
        //const personIdRegex = /\/internal\/users\/\d+/g
        const personIdRegex = /id=\"individual\-\d+/g
        //const personNameRegex = /\/internal\/users\/\d+\"\>\w+(\s\w+)*/g
        const personNameRegex = /class=\"entity_edit\"\>\w+(\s\w+)*/g
        let personUrlArray = [...description.matchAll(personUrlRegex)];
        if (personUrlArray && personUrlArray.length > 0) {
            for (let personUrl of personUrlArray) {
                let personIdArray = [...personUrl[0].matchAll(personIdRegex)];
                let personIdStr = personIdArray[0][0]
                let personId = personIdStr.substring(15)
                let personArray = [...personUrl[0].matchAll(personNameRegex)];
                let personFound = personArray[0][0]
                //let person = personFound.replace(/id=\"individual\-\d+\"\>/g, String(''));
                let person = personFound.replace(/class=\"entity_edit\"\>/g, String(''));
                let replacementVal = `{{ "person_id": "${personId}", "full_name": "${person}" }}`
                parsedText = parsedText.replace(personUrl[0], replacementVal).replace(/\&nbsp\;/g, ' ');
            }
        }
        // artifact transform
        const artifactUrlRegex = /\<span contenteditable\=\"false\" id=\"\w+\_artifact\-\d+\" class=\"entity_edit\"\>\w+(\s\w+)*\<\/span\>/g
        const artifactIdRegex = /id=\"\w+\_\w+\-\d+/g
        //const artifactIdRegex = /\w+\_\w+\-\d+/g
        const artifactIdentifierRegex = /class=\"entity_edit\"\>\w+(\s\w+)*/g
        let artifactUrlArray = [...description.matchAll(artifactUrlRegex)];
        if (artifactUrlArray && artifactUrlArray.length > 0) {
            for (let artifactUrl of artifactUrlArray) {
                let artifactIdArray = [...artifactUrl[0].matchAll(artifactIdRegex)];
                let artifactIdStr = artifactIdArray[0][0];
                let artifactTypeIncludingId = artifactIdStr.split("-")[0];
                let artifactType = artifactTypeIncludingId.substring(4)
                let artifactId = artifactIdStr.split("-")[1];
                //let id = idStrTrunc.substring(
                let identifierArray = [...artifactUrl[0].matchAll(artifactIdentifierRegex)];
                let identifierFound = identifierArray[0][0];
                let identifier = identifierFound.replace(/class=\"entity_edit\"\>/g, String(''));
                let replacementVal = `{{ "${artifactType}_id": "${artifactId}", "identifier": "${identifier}" }}`
                parsedText = parsedText.replace(artifactUrl[0], replacementVal).replace(/\&nbsp\;/g, ' ');
            }
        }
        return parsedText;
    },
    tokenToHtml: function(description) {
        let parsedText = description;
        // Person transform
        const personTokenRegex = /\{\{ \"person\_id\"\: \"\d+\"\, \"full\_name\"\: \"\w+(\s\w+)*\" \}\}/g;
        const personIdRegex = /\{\{ \"person\_id\"\: \"\d+/g;
        // const personNameRegex = /\"full\_name\"\: \"\w+ \w+/g;
        const personNameRegex = /\"full\_name\"\: \"\w+(\s\w+)*/g;
        let personTokenArray = [...description.matchAll(personTokenRegex)];
        for (let personToken of personTokenArray) {
            let personIdArray = [...personToken[0].matchAll(personIdRegex)];
            let personIdStr = personIdArray[0][0]
            let personId = personIdStr.substring(17)
            let nameArray = [...personToken[0].matchAll(personNameRegex)];
            if (nameArray && nameArray.length > 0) {
                let nameStr = nameArray[0][0]
                let fullName = nameStr.substring(14)
                parsedText = parsedText.replace(
                    personToken[0],
                    //`<a contenteditable="false" target="_blank" href="/internal/users/${id}">${fullName}</a>`
                    `<span contenteditable="false" id="individual-${personId}" class="entity_edit">${fullName}</span>`
                );
            }
        }
        // Artifact transform
        //const artifactTokenRegex = /\{\{ \"artifact\_id\"\: \"\d+\"\, \"identifier\"\: \"\w+(\s\w+)*\" \}\}/g;
        const artifactTokenRegex = /\{\{ \"\w+\_artifact\_id\"\: \"\d+\"\, \"identifier\"\: \"\w+(\s\w+)*\" \}\}/g;
        const artifactIdRegex = /\w+\_artifact\_id\"\: \"\d+/g;
        //const artifactIdRegex = /artifact\_id\"\: \"\d+/g;
        const artifactIdentifierRegex = /\"identifier\"\: \"\w+(\s\w+)*/g
        let artifactTokenArray = [...description.matchAll(artifactTokenRegex)];
        for (let artifactToken of artifactTokenArray) {
            let artifactIdArray = [...artifactToken[0].matchAll(artifactIdRegex)];
            let artifactIdStr = artifactIdArray[0][0]
            let artifactType = artifactIdStr.split("_")[0] + "_artifact";
            let artifactIdStrTrunc = artifactIdStr.split("_")[2];
            let artifactId = artifactIdStrTrunc.substring(6)
            let identifierArray = [...artifactToken[0].matchAll(artifactIdentifierRegex)];
            if (identifierArray && identifierArray.length > 0) {
                let identifierStr = identifierArray[0][0]
                let identifier = identifierStr.substr(15)
                let elemId = artifactType + "-" + artifactId;
                parsedText = parsedText.replace(
                    artifactToken[0],
                    `<span contenteditable="false" id="${elemId}" class="entity_edit">${identifier}</span>`
                    );
            }
        }
        return parsedText
    },
    openModalEntityEdit: function(e) {
        console.log(e)
        let entityDataType = e.target.id.split("-")[0]
        let entityId = e.target.id.split("-")[1]
        //this.rowNumberSelected = e.target.id.split("-")[2]
        console.log(entityDataType)
        console.log(entityId)
        if (entityId) {
            entityId = parseInt(entityId, 10);
        }
        this.entityEdit = {
            "data_type": entityDataType,
            "id": entityId,
        }
        if (['physical_artifact', 'document_artifact'].includes(entityDataType)) {
            this.tabSelected = 'artifact';
        } else if (entityDataType === 'individual') {
            this.tabSelected = 'person';
        }

        this.openPersonOrArtifact();
    },
    addEventListeners: function() {
      let vm = this;
      let runningSheetTable = $('#running-sheet-table');
      console.log(runningSheetTable)
      runningSheetTable.on(
          'keydown',
          (e) => {
              //this.runningSheetKeydown(e, window.getSelection().getRangeAt(0).startOffset);
              //e.preventDefault();
              this.runningSheetKeydown(e);
          });
      runningSheetTable.on(
          'keyup',
          (e) => {
              //e.preventDefault();
              this.runningSheetKeyup(e)
          });
      runningSheetTable.on(
          'click',
          '.row_delete',
          (e) => {
              this.runningSheetRowDelete(e)
          });
      runningSheetTable.on(
          'click',
          '.entity_edit',
          (e) => {
              this.openModalEntityEdit(e)
          });

      runningSheetTable.on(
          'click',
          '.row_history',
          (e) => {
              this.runningSheetRowHistory(e)
          });
      runningSheetTable.on(
          'click',
          '.row_reinstate',
          (e) => {
              this.runningSheetRowReinstate(e)
          });

      runningSheetTable.on(
          'paste',
          (e) => {
              console.log("plain text only");
              // cancel paste
              e.preventDefault();
              // get text representation of clipboard
              let text = (e.originalEvent || e).clipboardData.getData('text/plain');
              let transformedText = text.replace(/\n/g,'<br/>')
              // insert text manually
              document.execCommand("insertHTML", false, transformedText);
          });

      window.addEventListener('beforeunload', this.leaving);
      window.addEventListener('onblur', this.leaving);
    },
    runningSheetRowDelete: async function(e) {
        this.showSpinner = true;
        console.log(e)
        let rowNumber = e.target.id.replace('D', '-');
        console.log(rowNumber)
        console.log("runningSheetRowDelete")
        let running_sheet_id = null;
        for (let r of this.legal_case.running_sheet_entries) {
            if (r.number === rowNumber) {
                running_sheet_id = r.id
            }
        }
        let returnedEntry = await Vue.http.post(
            helpers.add_endpoint_join(
                api_endpoints.legal_case,
                this.legal_case.id + '/delete_reinstate_running_sheet_entry/',
            ),
            {
                "running_sheet_id": running_sheet_id,
                "deleted": true,
            }
            );
        if (returnedEntry.ok) {
            // required for running_sheet_history
            await this.setRunningSheetEntry(returnedEntry.body);
            let i = 0;
            for (let r of this.runningSheetUrl) {
                if (r.number === rowNumber) {
                    this.runningSheetUrl.splice(i, 1, returnedEntry.body);
                    this.runningSheetUrl[i].description = this.tokenToHtml(this.runningSheetUrl[i].description);
                }
                i += 1
            }
            this.constructRunningSheetTableEntry(rowNumber);

        }
        this.showSpinner = false;
    },
    runningSheetRowReinstate: async function(e) {
        this.showSpinner = true;
        console.log(e)
        let rowNumber = e.target.id.replace('R', '-');
        console.log(rowNumber)
        console.log("runningSheetRowReinstate")
        let running_sheet_id = null;
        for (let r of this.legal_case.running_sheet_entries) {
            if (r.number === rowNumber) {
                running_sheet_id = r.id
            }
        }
        let returnedEntry = await Vue.http.post(
            helpers.add_endpoint_join(
                api_endpoints.legal_case,
                this.legal_case.id + '/delete_reinstate_running_sheet_entry/',
            ),
            {
                "running_sheet_id": running_sheet_id,
                "deleted": false,
            }
            );
        if (returnedEntry.ok) {
            // required for running_sheet_history
            await this.setRunningSheetEntry(returnedEntry.body);
            let i = 0;
            for (let r of this.runningSheetUrl) {
                if (r.number === rowNumber) {
                    this.runningSheetUrl.splice(i, 1, returnedEntry.body);
                    this.runningSheetUrl[i].description = this.tokenToHtml(this.runningSheetUrl[i].description);
                }
                i += 1
            }
            this.constructRunningSheetTableEntry(rowNumber);
        }
        this.showSpinner = false;
    },
    runningSheetRowHistory: function(e) {
        console.log(e)
        let rowNumber = e.target.id.replace('H', '-');
        console.log(rowNumber)
        console.log("runningSheetRowHistory")
        this.runningSheetHistoryEntryInstance = rowNumber;
        this.setRunningSheetHistoryEntryBindId()
        this.$nextTick(() => {
            this.$refs.running_sheet_history.isModalOpen = true;
        });
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
        let copiedLegalCase = {};
        Object.getOwnPropertyNames(this.legal_case).forEach(
            (val, idx, array) => {
                if (this.hashAttributeWhitelist.includes(val)) {
                    copiedLegalCase[val] = this.legal_case[val]
                }
            });
        this.addHashAttributes(copiedLegalCase);
        if(this.objectHash !== hash(copiedLegalCase)){
            changed = true;
        }
        if (this.runningSheetEntriesUpdated.length > 0) {
            changed = true;
        }
        return changed;
    },
    calculateHash: function() {
        let copiedLegalCase = {}
        Object.getOwnPropertyNames(this.legal_case).forEach(
            (val, idx, array) => {
                if (this.hashAttributeWhitelist.includes(val)) {
                    copiedLegalCase[val] = this.legal_case[val]
                }
            });
        this.addHashAttributes(copiedLegalCase);
        this.objectHash = hash(copiedLegalCase);
    },
    addHashAttributes: function(obj) {
        let copiedRendererFormData = Object.assign({}, this.renderer_form_data);
        obj.renderer_form_data = copiedRendererFormData;
        return obj;
    },
    updateAssignedToId: async function (body) {
        await this.setLegalCase(body);
        this.constructRunningSheetTableWrapper();
        this.assignmentKey += 1;
    },
    constructRunningSheetTableWrapper: function() {
        this.runningSheetUrl = _.cloneDeep(this.legal_case.running_sheet_entries);
        console.log('this.runningSheetUrl');
        console.log(this.runningSheetUrl);
        let i = 0;
        for (let r of this.legal_case.running_sheet_entries) {
            let description = this.tokenToHtml(r.description)
            this.runningSheetUrl[i].description = description;
            i += 1;
        }
        this.$nextTick(() => {
            this.constructRunningSheetTable();
        });
    },
  },
  created: async function() {
      if (this.$route.params.legal_case_id) {
          await this.loadLegalCase({ legal_case_id: this.$route.params.legal_case_id });
      }
      await this.loadCurrentUser({ url: `/api/my_compliance_user_details` });
      //console.log(this)

      this.calculateHash();
      this.constructRunningSheetTableWrapper();
      /*
      if (this.legal_case && this.legal_case.boe_roi_options) {
          for (let item of this.legal_case.boe_roi_options) {
              let cloned_item = _.cloneDeep(item);
              this.boeRoiOptions.push(cloned_item)
          }
      }
      if (this.legal_case && this.legal_case.boe_other_statements_options) {
          for (let item of this.legal_case.boe_other_statements_options) {
              let cloned_item = _.cloneDeep(item);
              this.boeOtherStatementsOptions.push(cloned_item)
          }
      }
      */
  },
  destroyed: function() {
      window.removeEventListener('beforeunload', this.leaving);
      window.removeEventListener('onblur', this.leaving);
  },

  mounted: function() {
      this.$nextTick(() => {
          this.addEventListeners();
          // removes header from both brief_of_evidence and prosecution_brief
          $('.vue-treeselect__control').css("display", "none");
          /*
          if (this.openStatus) {
              this.constructRunningSheetTableWrapper();
          }
          */
          /*
          if (this.runningSheetVisibility) {
              this.constructRunningSheetTableWrapper();
          }
          */
      });
  },
};
</script>

<style lang="css">
.entity_edit {
    color: #337ab7;
}
.action-button {
    margin-top: 5px;
}
.new-row-button {
    margin-bottom: 5px;
    margin-right: 13px;
}
#close-button {
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
.inline-datatable {
  overflow-wrap: break-word;
}
</style>
