<template lang="html">
    <div class="container">
        <div class="row">
            <div class="col-md-3">
                <h3>Sanction Outcome: {{ displayLodgementNumber }}</h3>
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
                            :user_is_assignee="sanction_outcome.user_is_assignee"
                            :allowed_group_ids="sanction_outcome.allowed_groups"
                            :user_in_group="sanction_outcome.user_in_group" 
                            :assigned_to_id="sanction_outcome.assigned_to_id" 
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

                            <!-- Infringement Notice Coordinator -->
                            <div v-if="visibilityExtendDueDateButton" class="row action-button">
                                <div class="col-sm-12">
                                    <a @click="extendDueDate('')" class="btn btn-primary btn-block">
                                        Extend Due Date
                                    </a>
                                </div>
                            </div>

                            <div v-if="visibilityEscalateForWithdrawalButton" class="row action-button">
                                <div class="col-sm-12">
                                    <a @click="addWorkflow('escalate_for_withdrawal')" class="btn btn-primary btn-block">
                                        Escalate for Withdrawal
                                    </a>
                                </div>
                            </div>

                            <div v-if="visibilitySendParkingInfringementButton" class="row action-button">
                                <div class="col-sm-12">
                                    <a @click="sendParkingInfringement()" class="btn btn-primary btn-block">
                                        Endorse Parking Infringement
                                    </a>
                                </div>
                            </div>

                            <div v-if="visibilityRecordFerCaseNumberButton" class="row action-button">
                                <div class="col-sm-12">
                                    <a @click="recordFerCaseNumber('')" class="btn btn-primary btn-block">
                                        Record FER Case Number
                                    </a>
                                </div>
                            </div>

                            <!-- Branch Manager -->
                            <div v-if="visibilityReturnToInfringementNoticeCoordinatorButton" class="row action-button">
                                <div class="col-sm-12">
                                    <a @click="addWorkflow('return_to_infringement_notice_coordinator')" class="btn btn-primary btn-block">
                                        Return to<br />Infringement Notice Coordinator
                                    </a>
                                </div>
                            </div>
                            <div v-if="visibilityWithdrawByBranchManagerButton" class="row action-button">
                                <div class="col-sm-12">
                                    <a @click="addWorkflow('withdraw_by_branch_manager')" class="btn btn-primary btn-block">
                                        Withdraw
                                    </a>
                                </div>
                            </div>


                            <!-- Manager -->
                            <div v-if="visibilityWithdrawButtonForManager" class="row action-button">
                                <div class="col-sm-12">
                                    <a @click="addWorkflow('withdraw_by_manager')" class="btn btn-primary btn-block">
                                        Withdraw
                                    </a>
                                </div>
                            </div>
                            <div v-if="visibilityEndorseButton" class="row action-button">
                                <div class="col-sm-12">
                                    <a @click="addWorkflow('endorse')" class="btn btn-primary btn-block">
                                        Endorse
                                    </a>
                                </div>
                            </div>
                            <div v-if="visibilityDeclineButton" class="row action-button">
                                <div class="col-sm-12">
                                    <a @click="addWorkflow('decline')" class="btn btn-primary btn-block">
                                        Decline
                                    </a>
                                </div>
                            </div>
                            <div v-if="visibilityReturnToOfficerButton" class="row action-button">
                                <div class="col-sm-12">
                                    <a @click="addWorkflow('return_to_officer')" class="btn btn-primary btn-block">
                                        Return to Officer
                                    </a>
                                </div>
                            </div>

                            <!-- Officer -->
                            <div v-if="visibilitySendToManagerButton" class="row action-button">
                                <div class="col-sm-12">
                                    <a @click="addWorkflow('send_to_manager')" class="btn btn-primary btn-block">
                                        Send to Manager
                                    </a>
                                </div>
                            </div>
                            <div v-if="visibilityMarkDocumentPostedButton" class="row action-button">
                                <div class="col-sm-12">
                                    <a @click="addWorkflow('mark_document_posted')" class="btn btn-primary btn-block">
                                        Mark Document Posted
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
                            <li class="nav-item active"><a data-toggle="tab" :href="'#'+soTab">{{ typeDisplay }}</a></li>
                            <li class="nav-item" v-show="displayRemediationActions"><a data-toggle="tab" :href="'#'+raTab">Remediation Actions</a></li>
                            <li class="nav-item"><a data-toggle="tab" :href="'#'+deTab">Details</a></li>
                            <li class="nav-item"><a data-toggle="tab" :href="'#'+reTab">Related Items</a></li>
                        </ul>
                        <div class="tab-content">
                            <div :id="soTab" class="tab-pane fade in active">
                                <FormSection :formCollapse="false" :label="typeDisplay" Index="1">
                                    <div class="form-group"><div class="row">
                                        <div class="col-sm-3">
                                            <label>Identifier</label>
                                        </div>
                                        <div class="col-sm-6">
                                            <input :readonly="readonlyForm" class="form-control" v-model="sanction_outcome.identifier"/>
                                        </div>
                                    </div></div>

                                    <div class="form-group"><div class="row">
                                        <div class="col-sm-3">
                                            <label>Offence</label>
                                        </div>
                                        <div class="col-sm-6">
                                            <input readonly="true" class="form-control" v-model="displayOffence"/>
                                        </div>
                                    </div></div>

                                    <div class="form-group"><div class="row">
                                        <div class="col-sm-3">
                                            <label>Offender</label>
                                        </div>
                                        <div class="col-sm-6">

                                            <div v-if="sanction_outcome && sanction_outcome.offence && sanction_outcome.offence.offenders">
                                                <select :disabled="readonlyForm" class="form-control" v-model="sanction_outcome.offender">
                                                    <option value=""></option>
                                                    <option v-for="offender in sanction_outcome.offence.offenders" v-bind:value="offender" v-bind:key="offender.id">
                                                        <span v-if="offender.person">
                                                            {{ offender.person.first_name + ' ' + offender.person.last_name + ', DOB:' + offender.person.dob }}
                                                        </span>
                                                        <span v-else-if="offender.organisation">
                                                            {{ offender.organisation.name + ', ABN: ' + offender.organisation.abn }}
                                                        </span>
                                                    </option>
                                                </select>
                                            </div>

                                        </div>
                                    </div></div>

                                    <div class="form-group"><div class="row">
                                        <div class="col-sm-3">
                                            <label>Vehicle Registration Number</label>
                                        </div>
                                        <div class="col-sm-6">
                                            <input :readonly="readonlyForm" class="form-control" v-model="sanction_outcome.registration_number"/>
                                        </div>
                                    </div></div>

                                    <div class="form-group"><div class="row">
                                        <div class="col-sm-5">
                                            <label>Alleged committed offence</label>
                                        </div>
                                            <!--
                                        <div class="col-sm-6" v-for="item in sanction_outcome.alleged_offences">
                                            <input :readonly="readonlyForm" class="form-control" v-model="item.act + ', ' + item.name + ', ' + item.offence_text"/>
                                        </div>
                                            -->
                                        <div class="col-sm-12 form-group"><div class="row">
                                            <div class="col-sm-12">
                                                <datatable ref="alleged_committed_offence_table" id="alleged-committed-offence-table" :dtOptions="dtOptionsAllegedOffence" :dtHeaders="dtHeadersAllegedOffence" />
                                            </div>
                                        </div></div>

                                    </div></div>

                                    <div class="form-group"><div class="row">
                                        <div class="col-sm-3">
                                            <label>Issued on paper?</label>
                                        </div>
                                        <div class="col-sm-6">
                                            <input :disabled="readonlyForm" class="col-sm-1" id="issued_on_paper_yes" type="radio" v-model="sanction_outcome.issued_on_paper" :value="true" />
                                            <label class="col-sm-1 radio-button-label" for="issued_on_paper_yes">Yes</label>
                                            <input :disabled="readonlyForm" class="col-sm-1" id="issued_on_paper_no" type="radio" v-model="sanction_outcome.issued_on_paper" :value="false" />
                                            <label class="col-sm-1 radio-button-label" for="issued_on_paper_no">No</label>
                                        </div>
                                    </div></div>

                                       <div class="col-sm-12 form-group"><div class="row">
                                           <div class="col-sm-3">
                                               <label class="control-label pull-left">Paper ID</label>
                                           </div>
                                           <div class="col-sm-7">
                                               <input type="text" :readonly="readonlyForm" class="form-control" name="paper_id" placeholder="" v-model="sanction_outcome.paper_id" :disabled="!sanction_outcome.issued_on_paper" />
                                           </div>
                                       </div></div>

                                       <div class="col-sm-12 form-group"><div class="row">
                                           <div class="col-sm-3">
                                               <label class="control-label pull-left">Paper notice</label>
                                           </div>
                                           <div id="paper_id_notice">
                                               <div v-if="sanction_outcome.issued_on_paper" class="col-sm-7">
                                                   <filefield ref="sanction_outcome_file"
                                                              name="sanction-outcome-file"
                                                              :documentActionUrl="sanction_outcome.sanctionOutcomeDocumentUrl"
                                                              @update-parent="sanctionOutcomeDocumentUploaded"
                                                              :isRepeatable="true"
                                                              :readonly="readonlyForm" />
                                               </div>
                                           </div>
                                       </div></div>

                                </FormSection>
                            </div>

                            <div :id="raTab" class="tab-pane fade in">
                                <FormSection :formCollapse="false" label="Remediation Actions" Index="2">
                                    <div class="col-sm-12 form-group">
                                        <div class="row col-sm-12">
                                            <label class="control-label pull-left">Remediation Actions</label>
                                        </div>
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <datatable ref="tbl_remediation_actions" id="tbl_remediation_actions" :dtOptions="dtOptionsRemediationActions" :dtHeaders="dtHeadersRemediationActions" />
                                            </div>
                                        </div>
                                    </div>
                                </FormSection>
                            </div>

                            <div :id="deTab" class="tab-pane fade in">
                                <FormSection :formCollapse="false" label="Details" Index="3">
                                    <div class="form-group"><div class="row">
                                        <div class="col-sm-3">
                                            <label>Description</label>
                                        </div>
                                        <div class="col-sm-6">
                                            <textarea :disabled="readonlyForm" class="form-control" placeholder="add description" id="sanction-outcome-description" v-model="sanction_outcome.description"/>
                                        </div>
                                    </div></div>

                                    <div class="form-group"><div class="row">
                                        <div class="col-sm-3">
                                            <label>Date of Issue</label>
                                        </div>
                                        <!--
                                        <div class="col-sm-6">
                                            <input :readonly="readonlyForm" class="form-control" v-model="sanction_outcome.date_of_issue"/>
                                        </div>
                                        -->
                                        <div class="col-sm-3">
                                            <div class="input-group date" ref="dateOfIssuePicker">
                                                <input type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="sanction_outcome.date_of_issue" :disabled="!sanction_outcome.issued_on_paper || readonlyForm"/>
                                                <span class="input-group-addon">
                                                    <span class="glyphicon glyphicon-calendar"></span>
                                                </span>
                                            </div>
                                        </div>
                                    </div></div>

                                    <div class="form-group"><div class="row">
                                        <div class="col-sm-3">
                                            <label>Time of Issue</label>
                                        </div>
<!--
                                        <div class="col-sm-6">
                                            <input :readonly="readonlyForm" class="form-control" v-model="sanction_outcome.time_of_issue"/>
                                        </div>
-->

                                        <div class="col-sm-3">
                                            <div class="input-group date" ref="timeOfIssuePicker">
                                                <input type="text" class="form-control" placeholder="HH:MM" v-model="sanction_outcome.time_of_issue" :disabled="!sanction_outcome.issued_on_paper || readonlyForm" />
                                                <span class="input-group-addon">
                                                    <span class="glyphicon glyphicon-calendar"></span>
                                                </span>
                                            </div>
                                        </div>
                                    </div></div>
                                </FormSection>

                                <FormSection v-if="visibilityParkingInfringementSection" :formCollapse="false" label="Further Offender Details" Index="4">
                                    <div class="form-group"><div class="row">
                                        <div class="col-sm-3">
                                            <label>Registration Holder:</label>
                                        </div>
                                        <div class="col-sm-9">
                                            <RegistrationHolder
                                                :showClearPerson="true"
                                                :excludeStaff="true"
                                                :personOnly="true"
                                                :displayTitle="false"
                                                :isEditable="canUserEditParkingDetails"
                                                :parentEntity="registrationHolder"
                                                classNames="form-control"
                                                @entity-selected="registrationHolderSelected"
                                                @clear-person="clearRegistrationHolder"
                                                showCreateUpdate
                                                ref="search_registration_holder"
                                                domIdHelper="registration_holder"
                                                :key="registrationHolderBindId" />
                                        </div>
                                        <div class="col-sm-3">
                                            <label>Driver:</label>
                                        </div>
                                        <div class="col-sm-9">
                                            <Driver
                                                :showClearPerson="true"
                                                :excludeStaff="true"
                                                :personOnly="true"
                                                :displayTitle="false"
                                                :isEditable="canUserEditParkingDetails"
                                                :parentEntity="driver"
                                                classNames="form-control"
                                                @entity-selected="driverSelected"
                                                @clear-person="clearDriver"
                                                showCreateUpdate
                                                ref="search_driver"
                                                domIdHelper="driver"
                                                :key="updateDriverBindId" />
                                        </div>
                                    </div></div>
                                </FormSection>

                                <FormSection v-if="sanction_outcome.due_dates && sanction_outcome.due_dates.length>0" :formCollapse="false" label="Due Date" Index="5">
                                    <div v-for="item in sanction_outcome.due_dates">
                                        <div class="form-group"><div class="row">
                                            <div class="col-sm-3">
                                                <label>Payment due date:</label>
                                            </div>
                                            <div class="col-sm-3">
                                                <span>{{ formatDate(item.due_date_applied) }}</span>
                                            </div>
                                            <div class="col-sm-2">
                                                <label>Reason:</label>
                                            </div>
                                            <div class="col-sm-4">
                                                {{ item.reason_for_extension }}
                                            </div>
                                        </div></div>
                                    </div>
                                </FormSection>
                            </div>

                            <div :id="reTab" class="tab-pane fade in">
                                <FormSection :formCollapse="false" label="Related Items" Index="6">
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
            <SanctionOutcomeWorkflow
            ref="add_workflow"
            :workflow_type="workflow_type"
            :key="workflowBindId" />
        </div>

        <div v-if="extendPaymentDueDateInitialized">
            <ExtendPaymentDueDate
             ref="extend_payment_due_date"
             :due_date_1st="last_due_date_1st"
             :due_date_2nd="last_due_date_2nd"
             :due_date_max="sanction_outcome.due_date_extended_max"
             :key="extendDueDateBindId" />
        </div>

        <div v-if="recordFerCaseNumberInitialized">
            <RecordFerCaseNumber
             ref="record_fer_case_number"
             :key="recordFerCaseNumberBindId" />
        </div>

        <div v-if="sendParkingInfringementInitialized">
            <SendParkingInfringement
            ref="send_parking_infringement"
            :key="sendParkingInfringementBindId" />
        </div>

        <div v-if="acceptRemediationActionInitialized">
            <AcceptRemediationAction
             ref="accept_remediation_action"
             :remediation_action_id="remediation_action_id"
             @remediation_action_accepted="onRemediationActionUpdated"
             :key="acceptRemediationActionBindId" />
        </div>

        <div v-if="requestAmendmentRemediationAction">
            <RequestAmendmentRemediationAction
             ref="request_amendment_remediation_action"
             @remediation_action_updated="onRemediationActionUpdated"
             :remediation_action_id="remediation_action_id"
             :key="requestAmendmentRemediationActionBindId" />
        </div>
    </div>
</template>

<script>
import Vue from "vue";
import FormSection from "@/components/forms/section_toggle.vue";
import datatable from '@vue-utils/datatable.vue'
import utils from "@/components/external/utils";
import { api_endpoints, helpers, cache_helper } from "@/utils/hooks";
import { mapState, mapGetters, mapActions, mapMutations } from "vuex";
import Assignment from "../assignment.vue";
import CommsLogs from "@common-components/comms_logs.vue";
import filefield from '@/components/common/compliance_file.vue';
import SanctionOutcomeWorkflow from '@/components/internal/sanction_outcome/sanction_outcome_workflow';
import ExtendPaymentDueDate from '@/components/internal/sanction_outcome/extend_payment_due_date.vue';
import RecordFerCaseNumber from '@/components/internal/sanction_outcome/record_fer_case_number.vue';
import SendParkingInfringement from '@/components/internal/sanction_outcome/send_parking_infringement.vue';
import AcceptRemediationAction from '@/components/internal/sanction_outcome/accept_remediation_action.vue';
import RequestAmendmentRemediationAction from '@/components/internal/sanction_outcome/request_amendment_remediation_action.vue';
//import 'bootstrap/dist/css/bootstrap.css';
import hash from 'object-hash';
import RelatedItems from "@common-components/related_items.vue";
import RegistrationHolder from "@common-components/search_person_or_organisation.vue";
import Driver from "@common-components/search_person_or_organisation.vue";

export default {
    name: 'ViewSanctionOutcome',
    data() {
        let vm = this;
        vm.STATUS_DRAFT = 'draft';
        vm.STATUS_AWAITING_ENDORSEMENT = 'awaiting_endorsement';
        vm.STATUS_AWAITING_PRINT_AND_POST = 'awaiting_print_and_post';
        vm.STATUS_AWAITING_REVIEW = 'awaiting_review';
        vm.STATUS_AWAITING_AMENDMENT = 'awaiting_amendment';
        vm.STATUS_AWAITING_PAYMENT = 'awaiting_payment';
        vm.STATUS_WITH_DOT = 'with_dot';
        vm.STATUS_AWAITING_ISSUANCE = 'awaiting_issuance';
        vm.STATUS_DECLINED = 'declined';
        vm.STATUS_OVERDUE = 'overdue';
        vm.STATUS_ESCALATED_FOR_WITHDRAWAL = 'escalated_for_withdrawal';
        vm.STATUS_AWAITING_REMEDIATION_ACTIONS = 'awaiting_remediation_actions';
        vm.STATUS_WITHDRAWN = 'withdrawn'

        return {
            registrationHolderId: 0,
            driverId: 0,
            bindId: 0,
            sendParkingInfringementId: 0,
            ferCaseNumberId: 0,
            extendDueDateId: 0,
            temporary_document_collection_id: null,
            workflow_type :'',
            workflowBindId :'',
            remediation_action_id: 0,
            soTab: 'soTab' + this._uid,
            raTab: 'raTab' + this._uid,
            deTab: 'deTab' + this._uid,
            reTab: 'reTab' + this._uid,
            objectHash : null,
            extendPaymentDueDateInitialized: false,
            recordFerCaseNumberInitialized: false,
            sendParkingInfringementInitialized: false,
            acceptRemediationActionInitialized: false,
            requestAmendmentRemediationAction: false,
            hashAttributeWhitelist: [
                'alleged_committed_offences',
                'allocated_group_id',
                'date_of_issue',
                'description',
                'district_id',
                'identifier',
                'issued_on_paper',
                'offence',
                'offender',
                'paper_id',
                'paper_notices',
                'region_id',
                'time_of_issue',
                'type',
                'driver_id',
                'registration_holder_id',
            ],
            comms_url: helpers.add_endpoint_json(
                api_endpoints.sanction_outcome,
                this.$route.params.sanction_outcome_id + "/comms_log"
            ),
            comms_add_url: helpers.add_endpoint_json(
                api_endpoints.sanction_outcome,
                this.$route.params.sanction_outcome_id + "/add_comms_log"
            ),
            logs_url: helpers.add_endpoint_json(
                api_endpoints.sanction_outcome,
                this.$route.params.sanction_outcome_id + "/action_log"
            ),
            assign_url: helpers.add_endpoint_join(
                api_endpoints.sanction_outcome,
                this.$route.params.sanction_outcome_id + '/update_assigned_to_id/'
            ),
            assignmentKey: 0,
            dtHeadersRemediationActions: [
                "id",
                "Due Date",
                "Action Desc",
                "Status",
                "Action Taken",
                "Action",
            ],
            dtOptionsRemediationActions: {
                columns: [
                    {
                        data: 'id',
                        visible: false,
                        mRender: function(data, type, row){
                            return data;
                        }
                    },
                    {
                        data: 'due_date',
                        mRender: function(data, type, row) {
                            return moment(data).format("YYYY/MM/DD");
                        }
                    },
                    {
                        data: 'action',
                        mRender: function(data, type, row) {
                            return data;
                        }
                    },
                    {
                        data: 'status.name',
                    },
                    {
                        data: 'action_taken',
                        mRender: function(data, type, ra) {
                            let html = ''

                            let body = ''
                            let td = '<td col="row" class="action-taken-cell">'
                            let td_close = '</td>'
                            let th = '<th scope="col">'
                            let th_close = '</th>'

                            body += '<tr>' +
                                td + ra.action_taken + td_close +
                                td + ra.documents + td_close +
                            '</tr>'

                            let header = '<thead><tr>' +
                                th + 'Action Taken' + th_close +
                                th + 'Attachment' + th_close +
                                '</tr></thead>'
                            html = '<table class="table">' + header + body + '</table>'

                            return html
                        }
                    },
                    {
                        data: 'user_action',
                        mRender: function(data, type, row) {
                            return data;
                        }
                    },
                ]
            },
            dtHeadersAllegedOffence: [
                "id",
                "Act",
                "Section/Regulation",
                "Alleged Offence",
                "Action"
            ],
            dtOptionsAllegedOffence: {
                columns: [
                    {
                        data: "id",
                        visible: false
                    },
                    {
                        data: "Act",
                        mRender: function(data, type, row) {
                            let ret = data.alleged_offence.section_regulation.act;
                            if (!data.included){
                                ret = '<strike>' + ret + '</strike>';
                            }
                            return ret;
                        }
                    },
                    {
                        data: "Section/Regulation",
                        mRender: function(data, type, row) {
                            let ret = data.alleged_offence.section_regulation.name;
                            if (!data.included){
                                ret = '<strike>' + ret + '</strike>';
                            }
                            return ret;
                        }
                    },
                    {
                        data: "Alleged Offence",
                        mRender: function(data, type, row) {
                            let ret = data.alleged_offence.section_regulation.offence_text;
                            if (!data.included){
                                ret = '<strike>' + ret + '</strike>';
                            }
                            return ret;
                        }
                    },
                    {
                        data: "Action",
                        mRender: function(data, type, row) {
                            let ret = '';
                            if (!vm.readonlyForm && data.in_editable_status){
                                let checked_str = '';
                                let type_str = '';
                                let name_str = '';
                                let action_name = '';

                                if (vm.sanction_outcome.type.id == 'infringement_notice'){
                                    type_str = 'radio';
                                    name_str = ' name="aco_radio_group" ';
                                    if (data.included){
                                        checked_str = 'checked="checked"';
                                        action_name = '';
                                    } else {
                                        checked_str = '';
                                        action_name = 'Restore';
                                    }
                                } else {
                                    type_str = 'checkbox';
                                    name_str = ''
                                    if (data.included){
                                        checked_str = 'checked="checked"';
                                        action_name = 'Remove';
                                    } else {
                                        checked_str = '';
                                        action_name = 'Restore';
                                    }
                                }

                                ret = '<a><span class="include_alleged_committed_offence" data-alleged-committed-offence-id="' + data.id + '"/>' + action_name + '</span></a>';
                            }
                            return ret;
                        }
                    }
                ]
            }
        }
    },
    components: {
        FormSection,
        SanctionOutcomeWorkflow,
        CommsLogs,
        datatable,
        filefield,
        RelatedItems,
        ExtendPaymentDueDate,
        RecordFerCaseNumber,
        SendParkingInfringement,
        RegistrationHolder,
        AcceptRemediationAction,
        RequestAmendmentRemediationAction,
        Driver,
        Assignment,
    },
    created: async function() {
        if (this.$route.params.sanction_outcome_id) {
            await this.loadSanctionOutcome({ sanction_outcome_id: this.$route.params.sanction_outcome_id });
            this.createStorageAllegedCommittedOffences();
            this.constructAllegedCommittedOffencesTable();
            this.constructRemediationActionsTable();
            this.updateObjectHash()
        }
    },
    mounted: function() {
        this.$nextTick(() => {
            this.addEventListeners();
        });
    },
    computed: {
        ...mapGetters('sanctionOutcomeStore', {
            sanction_outcome: "sanction_outcome",
        }),
        acceptRemediationActionBindId: function() {
            return 'acceptRemediationActionBindId' + this.bindId
        },
        requestAmendmentRemediationActionBindId: function() {
            return 'requestAmendmentRemediationActionBindId' + this.bindId
        },
        displayRemediationActions: function() {
            if (this.sanction_outcome && this.sanction_outcome.type){
                return this.sanction_outcome.type.id == "remediation_notice" ? true : false;
            }
            return false;
        },
        registrationHolder: function() {
            let entity = {}
            if (this.sanction_outcome.registration_holder) {
                entity.id = this.sanction_outcome.registration_holder.id;
                entity.data_type = 'individual';
            }
            return entity;
        },
        driver: function() {
            let entity = {}
            if (this.sanction_outcome.driver) {
                entity.id = this.sanction_outcome.driver.id;
                entity.data_type = 'individual';
            }
            return entity;
        },
        registrationHolderBindId: function() {
            this.registrationHolderId += 1
            return 'resigtrationHolderBindId' + this.registrationHolderId;
        },
        updateDriverBindId: function() {
            this.driverId += 1
            return 'driverBindId' + this.driverId
        },
        last_due_date_1st: function() {
            let ret_value = null;
            if(this.sanction_outcome && this.sanction_outcome.due_dates && this.sanction_outcome.due_dates.length){
                ret_value = this.sanction_outcome.due_dates[this.sanction_outcome.due_dates.length - 1].due_date_1st;
            }
            return ret_value;
        },
        last_due_date_2nd: function() {
            let ret_value = null;
            if(this.sanction_outcome && this.sanction_outcome.due_dates && this.sanction_outcome.due_dates.length){
                ret_value = this.sanction_outcome.due_dates[this.sanction_outcome.due_dates.length - 1].due_date_2nd;
            }
            return ret_value;
        },
        recordFerCaseNumberBindId: function() {
            return 'record_fer_case_number_' + this.ferCaseNumberId;
        },
        sendParkingInfringementBindId: function() {
            return 'send_parking_infringement_' + this.sendParkingInfringementId;
        },
        extendDueDateBindId: function() {
            return 'extend_due_date_' + this.extendDueDateId;
        },
        relatedItemsBindId: function() {
            let timeNow = Date.now()
            if (this.sanction_outcome && this.sanction_outcome.id) {
                return 'sanction_outcome_' + this.sanction_outcome.id + '_' + this._uid;
            } else {
                return timeNow.toString();
            }
        },
        readonlyForm: function() {
            return !this.canUserEditForm;
        },
        canUserEditForm: function() {
            let canUserEdit = false;
            if (this.sanction_outcome.can_user_action){
                if (this.sanction_outcome.status.id === this.STATUS_AWAITING_AMENDMENT || this.sanction_outcome.status.id === this.STATUS_DRAFT){
                    canUserEdit = true;
                }
            }
            return canUserEdit;
        },
        canUserEditParkingDetails: function() {
            let canUserEdit = false;
            if (this.sanction_outcome.can_user_action){
                if (this.sanction_outcome.type.id === 'infringement_notice'){
                    if (this.sanction_outcome.status.id === this.STATUS_WITH_DOT ||
                        this.sanction_outcome.status.id === this.STATUS_AWAITING_ISSUANCE ||
                        this.sanction_outcome.status.id === this.STATUS_AWAITING_PAYMENT){
                        if (!this.sanction_outcome.offender){
                            canUserEdit = true;
                        }
                    }
                }
            }
            return canUserEdit;
        },
        statusDisplay: function() {
            let ret = '';
            if (this.sanction_outcome){
                if (this.sanction_outcome.status){
                    ret = this.sanction_outcome.status.name;
                }
            }
            return ret;
        },
        typeDisplay: function() {
            let ret = '';
            if (this.sanction_outcome){
                if (this.sanction_outcome.type){
                    ret = this.sanction_outcome.type.name;
                }
            }
            return ret;
        },
        displayOffence: function() {
            let ret = '';
            if (this.sanction_outcome){
                if (this.sanction_outcome.offence){
                    ret = this.sanction_outcome.offence.lodgement_number;
                }
            }
            return ret;
        },
        displayOffender: function() {
            let ret = '';
            if (this.sanction_outcome){
                if (this.sanction_outcome.offender){
                    if (this.sanction_outcome.offender.person){
                        ret = [this.sanction_outcome.offender.person.first_name, this.sanction_outcome.offender.person.last_name].filter(Boolean).join(" ");
                    } else if (this.sanction_outcome.offender.organisation){
                        ret = [this.sanction_outcome.offender.organisation.name, this.sanction_outcome.offender.organisation.abn].filter(Boolean).join(" ");
                    }
                }
            }
            return ret;
        },
        displayLodgementNumber: function() {
            let ret = '';
            if (this.sanction_outcome){
                ret = this.sanction_outcome.lodgement_number;
            }
            return ret;
        },
        visibilitySendParkingInfringementButton: function() {
            let visibility = false;

            if (this.sanction_outcome.can_user_action){
                if (this.sanction_outcome.type.id == 'infringement_notice' && this.sanction_outcome.is_parking_offence){
                    if (this.sanction_outcome.status.id === this.STATUS_AWAITING_ISSUANCE ||
                        this.sanction_outcome.status.id === this.STATUS_AWAITING_PAYMENT){
                        if (this.sanction_outcome.registration_holder_id || this.sanction_outcome.driver_id){
                            visibility = true;
                        }
                    }
                }
            }

            return visibility;
        },
        visibilityReturnToInfringementNoticeCoordinatorButton: function() {
            let visibility = false;
            if (this.sanction_outcome.can_user_action){
                if (this.sanction_outcome.status.id === this.STATUS_ESCALATED_FOR_WITHDRAWAL){
                    visibility = true;
                }
            }
            return visibility;
        },
        visibilityWithdrawByBranchManagerButton: function() {
            let visibility = false;
            if (this.sanction_outcome.can_user_action){
                if (this.sanction_outcome.status.id === this.STATUS_ESCALATED_FOR_WITHDRAWAL){
                    visibility = true;
                }
            }
            return visibility;
        },
        visibilityRecordFerCaseNumberButton: function() {
            let visibility = false;
            if (this.sanction_outcome.can_user_action){
                if (this.sanction_outcome.status.id === this.STATUS_OVERDUE){
                    visibility = true;
                }
            }
            return visibility;
        },
        visibilitySaveButton: function() {
            let visibility = false;
            if (this.sanction_outcome.can_user_action){
                if (this.sanction_outcome.status.id === this.STATUS_DRAFT || this.sanction_outcome.status.id === this.STATUS_AWAITING_AMENDMENT){
                    visibility = true;
                }
                if (this.canUserEditParkingDetails){
                    visibility = true;
                }
            }
            return visibility;
        },
        visibilityWithdrawButtonForManager: function() {
            let visibility = false;
            if (this.sanction_outcome.can_user_action){
                if (this.sanction_outcome.type.id == 'infringement_notice'){
                    if (this.sanction_outcome.status.id === this.STATUS_AWAITING_ENDORSEMENT && this.sanction_outcome.issued_on_paper){
                        // Manager can withdraw paper issued infringement notice
                        visibility = true;
                    }
                }
            }
            return visibility;
        },
        visibilityExtendDueDateButton: function() {
            let visibility = false;
            if (this.sanction_outcome.can_user_action){
                if (this.sanction_outcome.type.id == 'infringement_notice'){
                    if (this.sanction_outcome.status.id === this.STATUS_AWAITING_PAYMENT){
                        // This is when Infringement Notice Coordinator extends the due date
                        visibility = true;
                    }
                }
            }
            return visibility;
        },
       // visibilitySendToDotButton: function() {
       //     let visibility = false;
       //     if (this.sanction_outcome.can_user_action){
       //         if (this.sanction_outcome.type.id == 'infringement_notice'){
       //             if (this.sanction_outcome.status.id === this.STATUS_AWAITING_PAYMENT && this.sanction_outcome.is_parking_offence){
       //                 // This is when Infringement Notice Coordinator sends this IN to Dot
       //                 visibility = true;
       //             }
       //         }
       //     }
       //     return visibility;
       // },
        visibilityParkingInfringementSection: function() {
            let visibility = false;
            if (this.sanction_outcome.is_parking_offence){
                visibility = true;
            }
            return visibility;
        },
        visibilityEscalateForWithdrawalButton: function() {
            let visibility = false;
            if (this.sanction_outcome.can_user_action){
                if (this.sanction_outcome.type.id == 'infringement_notice'){
                    if (this.sanction_outcome.status.id === this.STATUS_AWAITING_PAYMENT){
                        // This is when Infringement Notice Coordinator withdraw
                        visibility = true;
                    }
                }
            }
            return visibility;
        },
        visibilitySendToManagerButton: function() {
            let visibility = false;
            if (this.sanction_outcome.can_user_action){
                if (this.sanction_outcome.status.id === this.STATUS_DRAFT || this.sanction_outcome.status.id === this.STATUS_AWAITING_AMENDMENT){
                    visibility = true;
                }
            }
            return visibility;
        },
        visibilityMarkDocumentPostedButton: function(){
            let visibility = false;
            if (this.sanction_outcome.can_user_action){
                if (this.sanction_outcome.status.id === this.STATUS_AWAITING_PRINT_AND_POST){
                    visibility = true;
                }
            }
            return visibility;
        },
        visibilityEndorseButton: function() {
            //return true;
            let visibility = false;
            if (this.sanction_outcome.can_user_action){
                if (this.sanction_outcome.status.id === this.STATUS_AWAITING_ENDORSEMENT || this.sanction_outcome.status.id === this.STATUS_AWAITING_REVIEW){
                    visibility = true;
                }
            }
            return visibility;
        },
        visibilityDeclineButton: function() {
            let visibility = false;
            if (this.sanction_outcome.can_user_action){
                if (this.sanction_outcome.status.id === this.STATUS_AWAITING_ENDORSEMENT || this.sanction_outcome.status.id === this.STATUS_AWAITING_REVIEW){
                    if (!this.sanction_outcome.issued_on_paper){
                        // Only sanction outcome not issued on paper can be declined, otherwise withdraw
                        visibility = true;
                    }
                }
            }
            return visibility;
        },
        visibilityReturnToOfficerButton: function() {
            let visibility = false;
            if (this.sanction_outcome.can_user_action){
                if (this.sanction_outcome.status.id === this.STATUS_AWAITING_REVIEW){
                    visibility = true;
                }
            }
            return visibility;
        }
    },
    methods: {
        ...mapActions('sanctionOutcomeStore', {
            loadSanctionOutcome: 'loadSanctionOutcome',
            saveSanctionOutcome: 'saveSanctionOutcome',
            setSanctionOutcome: 'setSanctionOutcome',
            setAssignedToId: 'setAssignedToId',
            setCanUserAction: 'setCanUserAction',
            setRelatedItems: 'setRelatedItems',
            setRegistrationHolder: 'setRegistrationHolder',
            setDriver: 'setDriver',
            loadRemediationAction: 'loadRemediationAction',
        }),
        clearRegistrationHolder: function(){
            console.log('clearRegistrationHolder');
            this.setRegistrationHolder({data_type: 'individual', id: null});
        },
        clearDriver: function() {
            console.log('clearDriver');
            this.setDriver({data_type: 'individual', id: null});
        },
        onRemediationActionUpdated: async function(remediation_action_id){_
            console.log('onRemediationActionUpdated');
            console.log(remediation_action_id);
            await this.loadRemediationAction({ remediation_action_id: remediation_action_id });
            this.constructRemediationActionsTable();
        },
        formatDate: function(d){
            console.log('formatDate');
            if (d === 'overdue'){
                return 'Overdue';
            }
            return moment(d).format("DD/MM/YYYY");
        },
        sendParkingInfringement: async function(){
            console.log('sendParkingInfringement()1');
            if (this.formChanged()){
                console.log('sendParkingInfringement()2');
                // Save changes implicitly
                await this.saveSanctionOutcome();
                this.updateObjectHash();
            }
            console.log('sendParkingInfringement()3');
            this.sendParkingInfringementId += 1
            this.sendParkingInfringementInitialized = true;
            this.$nextTick(() => {
                this.$refs.send_parking_infringement.isModalOpen = true;
            });
        },
        markDocumentPosted: function(){
            console.log('in markDocumentPosted')

        },
        driverSelected: function(data) {
            console.log(data);
            this.setDriver(data);
        },
        registrationHolderSelected: function(data) {
            console.log(data);
            this.setRegistrationHolder(data);
        },
        updateObjectHash: function() {
            this.objectHash = this.calculateHash();
        },
        calculateHash: function() {
            let copiedObject = {}
            Object.getOwnPropertyNames(this.sanction_outcome).forEach(
                (val, idx, array) => {
                    if (this.hashAttributeWhitelist.includes(val)) {
                        copiedObject[val] = this.sanction_outcome[val]
                    }
                });
            return hash(copiedObject);
        },
        formChanged: function(){
            let changed = false;
        //    if (!this.readonlyForm){
                if(this.objectHash !== this.calculateHash()){
                    changed = true;
                }
         //   }
            return changed;
        },
        sanctionOutcomeDocumentUploaded: function() {
            console.log('sanctionOutcomeDocumentUploaded');
        },
        createStorageAllegedCommittedOffences: function() {
            if (this.sanction_outcome && this.sanction_outcome.alleged_committed_offences){
                for (let i=0; i<this.sanction_outcome.alleged_committed_offences.length; i++){
                    // We need to know if this alleged commited offence is already included in the sanction outcome
                    // to manage Action column
                    this.sanction_outcome.alleged_committed_offences[i].already_included = this.sanction_outcome.alleged_committed_offences[i].included;
                }
            }
        },
        save: async function() {
            try {
                console.log('save()');
                let returned_so = await this.saveSanctionOutcome();

                await swal("Saved", "The record has been saved", "success");

                this.constructAllegedCommittedOffencesTable();
                this.updateObjectHash()
            } catch (err) {
                this.processError(err);
            }
        },
        saveExit: async function() {
            try {
                await this.saveSanctionOutcome();
                await swal("Saved", "The record has been saved", "success");

                // remove redundant eventListeners
                window.removeEventListener('beforeunload', this.leaving);
                window.removeEventListener('onblur', this.leaving);

                this.$router.push({ name: 'internal-offence-dash' });
            } catch(err) {
                this.processError(err);
            }
        },
        processError: async function(err){
            let errorText = '';
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
            await swal("Error", errorText, "error");
        },
        destroyed: function() {
            window.removeEventListener('beforeunload', this.leaving);
            window.removeEventListener('onblur', this.leaving);
        },
        setUpDateTimePicker: function() {
            let vm = this;
            let el_issue_date = $(vm.$refs.dateOfIssuePicker);
            let el_issue_time = $(vm.$refs.timeOfIssuePicker);

            // Issue "Date" field
            el_issue_date.datetimepicker({ format: "DD/MM/YYYY", maxDate: moment().millisecond(0).second(0).minute(0).hour(0), showClear: true });
            el_issue_date.on("dp.change", function(e) {
              if (el_issue_date.data("DateTimePicker").date()) {
                vm.sanction_outcome.date_of_issue = e.date.format("DD/MM/YYYY");
              } else if (el_issue_date.data("date") === "") {
                vm.sanction_outcome.date_of_issue = null;
              }
            });

            // Issue "Time" field
            el_issue_time.datetimepicker({ format: "LT", showClear: true });
            el_issue_time.on("dp.change", function(e) {
              if (el_issue_time.data("DateTimePicker").date()) {
                vm.sanction_outcome.time_of_issue = e.date.format("LT");
              } else if (el_issue_time.data("date") === "") {
                vm.sanction_outcome.time_of_issue = null;
              }
            });
        },
        addEventListeners: function() {
            this.setUpDateTimePicker();
            $("#alleged-committed-offence-table").on("click", ".remove_alleged_committed_offence", this.removeAllegedOffenceClicked);
            $("#alleged-committed-offence-table").on("click", ".restore_alleged_committed_offence", this.restoreAllegedOffenceClicked);
            $("#alleged-committed-offence-table").on("click", ".include_alleged_committed_offence", this.includeAllegedOffenceClicked);
            $("#tbl_remediation_actions").on("click", ".accept_remediation_action", this.acceptRemediationActionClicked);
            $("#tbl_remediation_actions").on("click", ".request_amendment_remediation_action", this.requestAmendmentRemediationActionClicked);

            window.addEventListener('beforeunload', this.leaving);
            window.addEventListener('onblur', this.leaving);
        },
        acceptRemediationActionClicked: function(e){
            let remediationActionId = parseInt(e.target.getAttribute("data-id"));
            this.remediation_action_id = remediationActionId;
            this.bindId += 1
            this.acceptRemediationActionInitialized = true;
            this.$nextTick(() => {
                this.$refs.accept_remediation_action.isModalOpen = true;
            });
        },
        requestAmendmentRemediationActionClicked: function(e){
            let remediationActionId = parseInt(e.target.getAttribute("data-id"));
            this.remediation_action_id = remediationActionId;
            this.bindId += 1
            this.requestAmendmentRemediationAction = true;
            this.$nextTick(() => {
                this.$refs.request_amendment_remediation_action.isModalOpen = true;
            });
        },
        leaving: function(e) {
            console.log('leaving');
            let vm = this;
            let dialogText = 'You have some unsaved changes.';
            if (vm.formChanged()){
                e.returnValue = dialogText;
                return dialogText;
            }
        },
        removeAllegedOffenceClicked: function(e) {
            let acoId = parseInt(e.target.getAttribute("data-alleged-committed-offence-id"));
            for (let i=0; i<this.sanction_outcome.alleged_committed_offences.length; i++){
                if(acoId == this.sanction_outcome.alleged_committed_offences[i].id){
                    //this.sanction_outcome.alleged_committed_offences[i].removed = true;
                    this.sanction_outcome.alleged_committed_offences[i].included = false;
                }
            }
            this.constructAllegedCommittedOffencesTable();
        },
        includeAllegedOffenceClicked: function(e){
            let acoId = parseInt(e.target.getAttribute("data-alleged-committed-offence-id"));
            if(this.sanction_outcome.type.id == 'infringement_notice'){
                // Set false to all the alleged committed offences
                for (let i=0; i<this.sanction_outcome.alleged_committed_offences.length; i++){
                    this.sanction_outcome.alleged_committed_offences[i].included = false;
                }
                // Set true to the alleged committed offence clicked
                for (let i=0; i<this.sanction_outcome.alleged_committed_offences.length; i++){
                    if(acoId == this.sanction_outcome.alleged_committed_offences[i].id){
                        this.sanction_outcome.alleged_committed_offences[i].included = true
                    }
                }
            } else {
                for (let i=0; i<this.sanction_outcome.alleged_committed_offences.length; i++){
                    if(acoId == this.sanction_outcome.alleged_committed_offences[i].id){
                        this.sanction_outcome.alleged_committed_offences[i].included = !this.sanction_outcome.alleged_committed_offences[i].included;
                    }
                }
            }
            this.constructAllegedCommittedOffencesTable();
        },
        restoreAllegedOffenceClicked: function(e){
            let acoId = parseInt(e.target.getAttribute("data-alleged-committed-offence-id"));
            for (let i=0; i<this.sanction_outcome.alleged_committed_offences.length; i++){
                if(acoId == this.sanction_outcome.alleged_committed_offences[i].id){
                    //this.sanction_outcome.alleged_committed_offences[i].removed = false;
                    this.sanction_outcome.alleged_committed_offences[i].included = true;
                }
            }
            this.constructAllegedCommittedOffencesTable();
        },
        constructRemediationActionsTable: function(){
            this.$refs.tbl_remediation_actions.vmDataTable.clear().draw();
            if (this.sanction_outcome.remediation_actions) {
                for(let i=0; i < this.sanction_outcome.remediation_actions.length; i++){
                    let ra = this.sanction_outcome.remediation_actions[i];
                    this.addRemediationActionToTable(ra);
                }
            }
        },
        constructAllegedCommittedOffencesTable: function(){
            this.$refs.alleged_committed_offence_table.vmDataTable.clear().draw();
            if (this.sanction_outcome.alleged_committed_offences){
                for(let i=0; i<this.sanction_outcome.alleged_committed_offences.length; i++){
                    this.addAllegedOffenceToTable(this.sanction_outcome.alleged_committed_offences[i]);
                }
            }
        },
        addRemediationActionToTable: function(remediation_action){
            this.$refs.tbl_remediation_actions.vmDataTable.row.add(remediation_action).draw();
        },
        addAllegedOffenceToTable: function(allegedCommittedOffence){
            this.$refs.alleged_committed_offence_table.vmDataTable.row.add({
                id: allegedCommittedOffence,
                Act: allegedCommittedOffence,
                "Section/Regulation": allegedCommittedOffence,
                "Alleged Offence": allegedCommittedOffence,
                Action: allegedCommittedOffence,
            }).draw();
        },
        addWorkflow(workflow_type) {
            this.workflow_type = workflow_type;
            this.updateWorkflowBindId();
            this.$nextTick(() => {
                this.$refs.add_workflow.isModalOpen = true;
            });
        },
        recordFerCaseNumber() {
            this.ferCaseNumberId += 1;
            this.recordFerCaseNumberInitialized = true;
            this.$nextTick(() => {
                this.$refs.record_fer_case_number.isModalOpen = true;
            });
        },
        extendDueDate() {
            this.extendDueDateId += 1;
            this.extendPaymentDueDateInitialized = true;
            this.$nextTick(() => {
                this.$refs.extend_payment_due_date.isModalOpen = true;
            });
        },
        updateWorkflowBindId: function() {
            let timeNow = Date.now()
            if (this.workflow_type) {
                this.workflowBindId = this.workflow_type + '_' + timeNow.toString();
            } else {
                this.workflowBindId = timeNow.toString();
            }
        },
        updateAssignedToId: async function (body) {
            this.setSanctionOutcome(body);
            //this.setAssignedToId(body.assigned_to_id);
            //this.setCanUserAction(body.can_user_action);
            this.updateObjectHash();
            this.assignmentKey += 1;
        },
    }
}
</script>

<style>
.action-taken-cell {
    max-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: initial !important;
}
</style>
