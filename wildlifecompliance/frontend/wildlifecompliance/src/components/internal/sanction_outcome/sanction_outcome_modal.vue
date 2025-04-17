<template lang="html">
    <div>
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="modalTitle" large force>
            <div class="container-fluid">
                <div class="col-sm-12 form-group"><div class="row">
                    <label class="col-sm-1">Type</label>
                    <div class="col-sm-4">
                        <!-- <select class="form-control" v-on:change="typeSelected($event)"> -->
                        <!-- <select class="form-control" v-on:change="typeSelected($event)" v-bind:value="sanction_outcome.type"> -->
                        <select class="form-control" v-model="sanction_outcome.type" @change="typeChanged()">
                            <option v-for="option in options_for_types" v-bind:value="option.id" v-bind:key="option.id">
                                {{ option.display }}
                            </option>
                        </select>
                    </div>
                </div></div>

                <div v-show="displayTabs">
                    <ul class="nav nav-pills">
                        <li class="nav-item active"><a data-toggle="tab" :href="'#'+nTab">{{ firstTabTitle }}</a></li>
                        <li class="nav-item" v-show="displayRemediationActions"><a data-toggle="tab" :href="'#'+aTab">Remediation Actions</a></li>
                        <li class="nav-item"><a data-toggle="tab" :href="'#'+dTab">Details</a></li>
                    </ul>
                    <div class="tab-content">
                        <div :id="nTab" class="tab-pane fade in active"><div class="row">

                            <div class="col-sm-12 form-group"><div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left" for="identifier">Identifier</label>
                                </div>
                                <div class="col-sm-7">
                                    <div v-show="sanction_outcome">
                                        <input type="text" class="form-control" name="identifier" placeholder="" v-model="sanction_outcome.identifier" >
                                    </div>
                                </div>
                            </div></div>

                            <div class="col-sm-12 form-group"><div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left">Region</label>
                                </div>
                                <div class="col-sm-7">
                                  <select class="form-control col-sm-9" v-on:change.prevent="sanction_outcome.region_id=$event.target.value; updateDistricts('updatefromUI')" v-bind:value="sanction_outcome.region_id">
                                    <option  v-for="option in regions" :value="option.id" v-bind:key="option.id">
                                      {{ option.name }}
                                    </option>
                                  </select>
                                </div>
                            </div></div>

                            <div class="col-sm-12 form-group"><div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left">District</label>
                                </div>
                                <div class="col-sm-7">
                                  <select class="form-control" v-model="sanction_outcome.district_id">
                                    <option  v-for="option in availableDistricts" :value="option.district_id" v-bind:key="option.district_id">
                                      {{ option.district_name }}
                                    </option>
                                  </select>
                                </div>
                            </div></div>

                            <div class="col-sm-12 form-group"><div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left">Offence</label>
                                </div>
                                <div class="col-sm-7">
                                    <div v-show="sanction_outcome">
                                        <select :disabled="offenceReadonly" class="form-control" v-on:change="currentOffenceChanged()" v-model="sanction_outcome.current_offence">
                                            <option value=""></option>
                                            <option v-for="option in options_for_offences" v-bind:value="option" v-bind:key="option.id">
                                                {{ option.lodgement_number + ': ' + option.identifier }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </div></div>

                            <div class="col-sm-12 form-group"><div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left">Offender</label>
                                </div>
                                <div class="col-sm-7">
                                    <div v-if="sanction_outcome && sanction_outcome.current_offence && sanction_outcome.current_offence.offenders">
                                        <!--
                                        <select class="form-control" @change="offenderSelected($event)" :value="sanction_outcome.current_offender.id" >
                                        -->
                                        <select class="form-control" v-model="sanction_outcome.current_offender" @change="currentOffenderChanged()">
                                            <option value=""></option>
                                            <option v-for="offender in sanction_outcome.current_offence.offenders"
                                                :value="offender"
                                                :key="offender.id">
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

                            <div class="col-sm-12 form-group"><div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left">Vehicle Registration Number</label>
                                </div>
                                <div class="col-sm-7">
                                    <input :disabled="!is_parking_offence" type="text" class="form-control" name="registration_number" placeholder="" v-model="sanction_outcome.registration_number" >
                                </div>
                            </div></div>

                            <div class="col-sm-12 form-group">
                                <div class="row col-sm-12">
                                    <label class="control-label pull-left">Alleged committed offences</label>
                                </div>
                                <div class="row">
                                    <div class="col-sm-12">
                                        <datatable ref="tbl_alleged_offence" id="tbl_alleged_offence" :dtOptions="dtOptionsAllegedOffence" :dtHeaders="dtHeadersAllegedOffence" />
                                    </div>
                                </div>
                            </div>

                            <div class="col-sm-12 form-group"><div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left">Issued on paper?</label>
                                </div>
                                <div class="col-sm-7">

                                  <input class="col-sm-1" id="issued_on_paper_yes" type="radio" v-model="sanction_outcome.issued_on_paper" :value="true" />
                                  <label class="col-sm-1 radio-button-label" for="issued_on_paper_yes">Yes</label>
                                  <input class="col-sm-1" id="issued_on_paper_no" type="radio" v-model="sanction_outcome.issued_on_paper" :value="false" />
                                  <label class="col-sm-1 radio-button-label" for="issued_on_paper_no">No</label>
                                </div>
                            </div></div>

                            <div class="col-sm-12 form-group"><div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left">Paper ID</label>
                                </div>
                                <div class="col-sm-7">
                                    <input type="text" class="form-control" name="paper_id" placeholder="" v-model="sanction_outcome.paper_id" :disabled="!sanction_outcome.issued_on_paper" />
                                </div>
                            </div></div>

                            <div class="col-sm-12 form-group"><div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left">Paper notice</label>
                                </div>
                                <div id="paper_id_notice">
                                    <div v-if="sanction_outcome.issued_on_paper" class="col-sm-7">
                                        <filefield
                                        ref="sanction_outcome_file"
                                        name="sanction-outcome-file"
                                        documentActionUrl="temporary_document"
                                        @update-temp-doc-coll-id="setTemporaryDocumentCollectionId"
                                        :isRepeatable="true"
                                        :disabled="!sanction_outcome.issued_on_paper"/>
                                    </div>
                                </div>
                            </div></div>

                        </div></div>

                        <div :id="aTab" class="tab-pane fade in"><div class="row">

                            <div class="col-sm-12 form-group"><div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left">Action</label>
                                </div>
                                <div class="col-sm-7">
                                    <textarea class="form-control" placeholder="add description" id="sanction-outcome-description" v-model="current_remediation_action.action" />
                                </div>
                            </div></div>

                            <div class="col-sm-12 form-group"><div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left">Due Date</label>
                                </div>
                                <div class="col-sm-3">
                                    <div class="input-group date" ref="dueDatePicker">
                                        <input type="text" class="form-control" placeholder="DD/MM/YYYY" :value="current_remediation_action.due_date" />
                                        <span class="input-group-addon">
                                            <span class="glyphicon glyphicon-calendar"></span>
                                        </span>
                                    </div>
                                </div>
                            </div></div>

                            <div class="col-sm-12 form-group"><div class="row">
                                <div class="col-sm-12">
                                    <input :disabled="!enableAddActionButton" type="button" class="btn btn-primary pull-right" value="Add" @click.prevent="addRemediationActionClicked()" />
                                </div>
                            </div></div>

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

                        </div></div>

                        <div :id="dTab" class="tab-pane fade in"><div class="row">
                            <div class="col-sm-12 form-group"><div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left">Description</label>
                                </div>
                                <div class="col-sm-7">
                                    <textarea class="form-control" placeholder="add description" id="sanction-outcome-description" v-model="sanction_outcome.description"/>
                                </div>
                            </div></div>

                            <div class="col-sm-12 form-group"><div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left">Date of Issue</label>
                                </div>
                                <div class="col-sm-3">
                                    <div class="input-group date" ref="dateOfIssuePicker">
                                        <input type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="sanction_outcome.date_of_issue" :disabled="!sanction_outcome.issued_on_paper"/>
                                        <span class="input-group-addon">
                                            <span class="glyphicon glyphicon-calendar"></span>
                                        </span>
                                    </div>
                                </div>
                            </div></div>

                            <div class="col-sm-12 form-group"><div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left">Time of Issue</label>
                                </div>
                                <div class="col-sm-3">
                                    <div class="input-group date" ref="timeOfIssuePicker">
                                        <input type="text" class="form-control" placeholder="HH:MM" v-model="sanction_outcome.time_of_issue" :disabled="!sanction_outcome.issued_on_paper" />
                                        <span class="input-group-addon">
                                            <span class="glyphicon glyphicon-calendar"></span>
                                        </span>
                                    </div>
                                </div>
                            </div></div>
                        </div></div>
                    </div>

                </div>
            </div>
            <div slot="footer">
                <div v-if="errorResponse" class="form-group">
                    <div class="row">
                        <div class="col-sm-12">
                            <strong><span style="white-space: pre;" v-html="errorResponse"></span></strong>
                        </div>
                    </div>
                </div>
                <button type="button" v-if="processingDetails" disabled class="btn btn-default" @click="ok"><i class="fa fa-spinner fa-spin"></i> Adding</button>
                <span v-else>
                    <button type="button" :disabled="!displaySendToManagerButton" class="btn btn-default" @click="ok">Send to Manager</button>
                </span>
                <button type="button" class="btn btn-default" @click="cancel">Cancel</button>
            </div>
        </modal>
    </div>
</template>

<script>
import Vue from "vue";
import modal from "@vue-utils/bootstrap-modal.vue";
import datatable from "@vue-utils/datatable.vue";
import filefield from "@/components/common/compliance_file.vue";
import { mapGetters, mapActions } from "vuex";
import { api_endpoints, helpers, cache_helper } from "@/utils/hooks";
import utils from "../utils";
import $ from "jquery";
import "jquery-ui/ui/widgets/draggable.js";
//import "bootstrap/dist/css/bootstrap.css";
import "awesomplete/awesomplete.css";

export default {
    name: "SanctionOutcome",
    data: function() {
      let vm = this;

    return {
        temporary_document_collection_id: null,
        nTab: "nTab" + vm._uid,
        aTab: "aTab" + vm._uid,
        dTab: "dTab" + vm._uid,
        isModalOpen: false,
        processingDetails: false,

        // regionDistricts: [],
        regions: [], // this is the list of options
        availableDistricts: [], // this is generated from the regionDistricts[] above
        documentActionUrl: null,
        elem_paper_id_notice: null,
        errorResponse: "",
        offenceReadonly: false,

        aco_ids_included: [],
        aco_ids_excluded: [],
        is_parking_offence: false,

        // This is the object to be sent to the server when saving
        sanction_outcome: {
            type: "",
            region_id: null,
            district_id: null,
            identifier: "",
            current_offence: {}, // Store an offence to be saved as an attribute of the sanction outcome
            // The offenders and the alleged_offences under this offence object are used
            // to construct a dropdown list for the offenders and the alleged offences datatable
            current_offender: {}, // Store an offender to be saved as an attribute of the sanction outcome
            issued_on_paper: false,
            paper_id: "",
            description: "",
            date_of_issue: null,
            time_of_issue: null,
            remediation_actions: []
        },
        current_remediation_action: {
          action: "",
          due_date: null
        },

        act_name_of_selected_ao: '',  // when the user ticks the first one, only other alleged offences from the same Act will be available.
                                      // No mixing of BCA and CALM

        // List for dropdown
        options_for_types: [],
        options_for_offences: [],

        dtHeadersAllegedOffence: [
          "id",
          "Act",
          "Section/Regulation",
          "Alleged Offence",
          "Include"
        ],
        dtOptionsAllegedOffence: {
          columns: [
            {
                visible: false,
                data: 'id',
                name: 'id',
                render: function(data, type, full){
                    return full.id;
                }
            },
            {
                data: 'id',
                name: 'id',
                render: function(data, type, full){
                    let ret = full.section_regulation.act;
                    if (full.removed){
                        ret = '<strike>' + ret + '</strike>';
                    }
                    return ret;
                }
            },
            {
                data: 'id',
                name: 'id',
                render: function(data, type, full){
                    let ret = full.section_regulation.name;
                    if (full.removed){
                        ret = '<strike>' + ret + '</strike>';
                    }
                    return ret;
                }
            },
            {
                data: 'id',
                name: 'id',
                render: function(data, type, full){
                    let ret = full.section_regulation.offence_text;
                    if (full.removed){
                        ret = '<strike>' + ret + '</strike>';
                    }
                    return ret;
                }
            },
            {
                data: 'id',
                name: 'id',
                render: function(data, type, full) {
                    console.log('full: ')
                    console.log(full)
                    let ret_line = '';

                    // Chenck if this alleged offence has already a connection to the current offender selected
                    let current_offender_has_connection = false;

                    // CALM and BCA should not be both included in a sanction outcome at the same time.
                    let unselectable = true
                    if (vm.sanction_outcome.type == 'infringement_notice'){
                        unselectable = false
                    } else if (!vm.act_name_of_selected_ao || vm.act_name_of_selected_ao == full.section_regulation.act){
                        unselectable = false
                    }
                    let selected_str = ''
                    if (vm.aco_ids_included.includes(full.id.toString())){
                        selected_str = 'checked="checked"'
                    }

                    if (full.connected || full.removed || unselectable){
                        // Disabled
                        if (vm.sanction_outcome.type == 'infringement_notice'){
                            ret_line += '<input type="radio" name="infringement_radio_button" class="alleged_offence_include" value="' + full.id + '" disabled></input>';
                        } else if (vm.sanction_outcome.type == '' || vm.sanction_outcome.type == null) {
                            // Should not reach here
                            ret_line += '';
                        } else {
                            ret_line += '<input type="checkbox" class="alleged_offence_include" value="' + full.id + '" disabled></input>';
                        }
                    } else {
                        // Enabled
                        if (vm.sanction_outcome.type == 'infringement_notice'){
                            ret_line += '<input type="radio" name="infringement_radio_button" class="alleged_offence_include" value="' + full.id + '"' + selected_str + '></input>';
                        } else if (vm.sanction_outcome.type == '' || vm.sanction_outcome.type == null) {
                            // Should not reach here
                            ret_line += '';
                        } else {
                            let disabled_str = ''
                            if (full.section_regulation.is_parking_offence){
                                disabled_str = ' disabled '
                                selected_str = ''
                            }
                            //ret_line += '<input type="checkbox" class="alleged_offence_include" value="' + full.id + '" checked="checked"></input>';
                            ret_line += '<input type="checkbox" class="alleged_offence_include" value="' + full.id + '"' + selected_str + disabled_str + '></input>';
                        }
                    }

                    return ret_line;
                }
            }
          ]
        },
        dtHeadersRemediationActions: ["id", "Due Date", "Action", "Action"],
        dtOptionsRemediationActions: {
          columns: [
            {
              data: "id",
              name: 'id',
              visible: false
            },
            {
              data: "due_date",
              name: 'id',
            },
            {
              data: "action_text",
              name: 'id',
            },
            {
              data: "id",
              name: 'id',
              render: function(data, type, row) {
                return (
                  '<a href="#" class="remove_button" data-remediation-action-id="' +
                  row.id +
                  '">Remove</a>'
                );
              }
            }
          ]
        }
      };
    },
    props:{
          workflow_type: {
              type: String,
              default: 'send_to_manager',
          },
    },
    components: {
      modal,
      datatable,
      filefield,
    },
    watch: {
        issued_on_paper: {
            handler: function(){
              let vm = this;
              if (!vm.sanction_outcome.issued_on_paper) {
                vm.sanction_outcome.date_of_issue = null;
                vm.sanction_outcome.time_of_issue = null;
                vm.elem_paper_id_notice.slideUp(500);
              } else {
                vm.elem_paper_id_notice.slideDown(500);
              }
            }
        },
      //  current_type: {
      //      handler: function() {
      //          this.typeChanged();
      //      }
      //  },
      //  current_offence: {
      //      handler: function() {
      //          this.currentOffenceChanged();
      //      }
      //  },
      //  current_offender: {
      //      handler: function() {
      //          this.currentOffenderChanged();
      //      }
      //  },
        current_region_id: {
            handler: function() {
                this.currentRegionIdChanged();
            }
        },
    },
    computed: {
        ...mapGetters("offenceStore", {
          offence: "offence"
        }),
        enableAddActionButton: function() {
            let enabled = false;
            if(this.current_remediation_action.action && this.current_remediation_action.due_date){
                enabled = true;
            }
            return enabled;
        },
        issued_on_paper: function() {
            return this.sanction_outcome.issued_on_paper;
        },
       // current_offence: function() {
       //     return this.sanction_outcome.current_offence;
       // },
       // current_offender: function() {
       //     return this.sanction_outcome.current_offender;
       // },
        current_region_id: function() {
            return this.sanction_outcome.region_id;
        },
       // current_type: function() {
       //     return this.sanction_outcome.type;
       // },
        modalTitle: function() {
            return "Identify Sanction Outcome";
        },
        firstTabTitle: function() {
            for (let i = 0; i < this.options_for_types.length; i++) {
                if (this.options_for_types[i]["id"] == this.sanction_outcome.type) {
                    return this.options_for_types[i]["display"];
                }
            }
            return "";
        },
        displayTabs: function() {
          return this.sanction_outcome.type == "" ? false : true;
        },
        displaySendToManagerButton: function() {
            let retValue = false;

            if (!this.processingDetails && this.sanction_outcome.type) {
                if (this.regionDistrictId) {
                    if ((this.sanction_outcome.issued_on_paper && this.sanction_outcome.date_of_issue) || !this.sanction_outcome.issued_on_paper) {
                        retValue = true;
                    }
                }
            }
            return retValue;
        },
        displayRemediationActions: function() {
          return this.sanction_outcome.type == "remediation_notice" ? true : false;
        },
        regionDistrictId: function() {
          if (
            this.sanction_outcome.district_id ||
            this.sanction_outcome.region_id
          ) {
            return this.sanction_outcome.district_id
              ? this.sanction_outcome.district_id
              : this.sanction_outcome.region_id;
          } else {
            return null;
          }
        },
        groupPermission: function() {
          return "manager"; // Send to manager
        },
    },
    methods: {
        ...mapActions('offenceStore', {
            loadOffence: 'loadOffence',
        }),
        aco_include_clicked: function() {
            console.log('in aco_include_clicked')
            let vm = this;
            vm.aco_ids_included = [];
            vm.aco_ids_excluded = [];
            let checkboxes = $(".alleged_offence_include");
            console.log(checkboxes)
            for (let i = 0; i < checkboxes.length; i++) {
                if (checkboxes[i].checked) {
                    vm.aco_ids_included.push(checkboxes[i].value);

                } else {
                    vm.aco_ids_excluded.push(checkboxes[i].value);
                }
            }
            if (vm.aco_ids_included.length){
                for (let alleged_offence of vm.sanction_outcome.current_offence.alleged_offences){
                    if (alleged_offence.id == vm.aco_ids_included[0]){
                        vm.act_name_of_selected_ao = alleged_offence.section_regulation.act
                    }
                }
            } else {
                // No alleged offences selected
                vm.act_name_of_selected_ao = ''
            }
            console.log('act_name_of_selected_ao: ' + vm.act_name_of_selected_ao)
            vm.check_if_is_parking_offence();
            vm.constructAllegedOffencesTable();
        },
        check_if_is_parking_offence: function() {
            this.is_parking_offence = false;
            if (this.sanction_outcome.type == 'infringement_notice' && this.aco_ids_included.length == 1){
                for (let i=0; i < this.sanction_outcome.current_offence.alleged_offences.length; i++){

                    console.log(this.sanction_outcome.current_offence.alleged_offences[i]);

                    if (this.sanction_outcome.current_offence.alleged_offences[i].id == this.aco_ids_included[0]){
                        if (this.sanction_outcome.current_offence.alleged_offences[i].section_regulation.is_parking_offence){
                            this.is_parking_offence = true
                        }
                    }
                }
            }
        },
        setTemporaryDocumentCollectionId: function(val) {
            this.temporary_document_collection_id = val;
        },
        ok: async function() {
            try{
                this.processingDetails = true;
                let response = await this.sendData();

                if(response.ok){
                    if (this.$parent.offence && this.offence.id) {
                        await this.loadOffence({
                            offence_id: this.offence.id,
                        });
                    }
                }

                this.close();
                this.processingDetails = false;
                this.$emit('sanction_outcome_created');
            } catch(err) {
                this.processError(err);
                this.processingDetails = false;
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
                        errorText += field_name + ': ';
                        for (let j=0; j<err.body[field_name].length; j++){
                            errorText += err.body[field_name][j] + '<br />';
                        }
                    }
                }
            }
            this.errorResponse = errorText;
            //await swal("Error", errorText, "error");
        },
        ...mapActions({
            loadAllocatedGroup: 'loadAllocatedGroup',  // defined in store/modules/user.js
        }),
        cancel: async function() {
            if(this.$refs.sanction_outcome_file) {
                await this.$refs.sanction_outcome_file.cancel();
            }
            this.close();
        },
        typeChanged: function(){
            console.log('typeChanged');
            this.constructAllegedOffencesTable();
            this.check_if_is_parking_offence();
        },
        makeModalsDraggable: function(){
            this.elem_modal = $('.modal > .modal-dialog');
            for (let i=0; i<this.elem_modal.length; i++){
                $(this.elem_modal[i]).draggable();
            }
        },
        close: function() {
            this.$parent.sanctionOutcomeInitialised = false;
            this.isModalOpen = false;
        },
        loadDefaultData: function() {
            if (this.$parent.call_email) {
                this.sanction_outcome.region_id = this.$parent.call_email.region_id;
                this.sanction_outcome.district_id = this.$parent.call_email.district_id;
            }

            if (this.$parent.inspection) {
                this.sanction_outcome.region_id = this.$parent.inspection.region_id;
                this.sanction_outcome.district_id = this.$parent.inspection.district_id;
            }

            if (this.$parent.offence) {
                this.sanction_outcome.region_id = this.$parent.offence.region_id;
                this.sanction_outcome.district_id = this.$parent.offence.district_id;
                for (let i = 0; i < this.options_for_offences.length; i++) {
                    if (this.options_for_offences[i].id == this.$parent.offence.id) {
                        this.sanction_outcome.current_offence = this.options_for_offences[i];
                        this.offenceReadonly = true;
                    }
                }
            }

            this.clearTableRemediationActions();
        },
        currentRegionIdChanged: function() {
          this.updateDistricts();
        },
        addRemediationActionClicked: function() {
          let vm = this;
          if (vm.current_remediation_action) {
            vm.$refs.tbl_remediation_actions.vmDataTable.row
              .add({
                id: helpers.guid(),
                due_date: moment(vm.current_remediation_action.due_date, "DD/MM/YYYY").format("DD/MM/YYYY"),
                action_text: vm.current_remediation_action.action
              })
              .draw();
            vm.current_remediation_action.action = "";
            vm.current_remediation_action.due_date = null;
          }
        },
        updateDistricts: function(updateFromUI) {
          if (updateFromUI) {
            // We don't want to clear the default district selection when initially loaded, which derived from the call_email
            this.sanction_outcome.district_id = null;
          }

          this.availableDistricts = []; // This is a list of options for district
          for (let region of this.regions) {
            if (region.id == this.offence.region_id) {
            this.availableDistricts = region.districts
            }
          }

          this.availableDistricts.splice(0, 0, {
            district_id: "",
            district_name: "",
            district: "",
            districts: [],
            region: null
          });
        },
        addEventListeners: function() {
            let vm = this;
            let el_issue_date = $(vm.$refs.dateOfIssuePicker);
            let el_issue_time = $(vm.$refs.timeOfIssuePicker);
            let el_due_date = $(vm.$refs.dueDatePicker);

            // Issue "Date" field
            el_issue_date.datetimepicker({
              format: "DD/MM/YYYY",
              maxDate: "now",
              showClear: true
            });
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

            // Due "Date" field
            el_due_date.datetimepicker({
              minDate: moment().millisecond(0).second(0).minute(0).hour(0),
              format: "DD/MM/YYYY",
              showClear: true
            });
            el_due_date.on("dp.change", function(e) {
              if (el_due_date.data("DateTimePicker").date()) {
                vm.current_remediation_action.due_date = e.date.format("DD/MM/YYYY");
              } else if (el_due_date.data("date") === "") {
                vm.current_remediation_action.due_date = null;
              }
            });

            $("#tbl_remediation_actions").on("click", ".remove_button", vm.removeClicked);
            $("#tbl_alleged_offence").on("click", ".alleged_offence_include", vm.aco_include_clicked);
        },
        removeClicked: function(e) {
          let vm = this;
          let remediationActionId = e.target.getAttribute(
            "data-remediation-action-id"
          );
          vm.$refs.tbl_remediation_actions.vmDataTable.rows(function(
            idx,
            data,
            node
          ) {
            if (data.id == remediationActionId) {
              vm.$refs.tbl_remediation_actions.vmDataTable
                .row(idx)
                .remove()
                .draw();
            }
          });
        },
        offenceSelected: function(e) {
          let vm = this;
          let offence_id = parseInt(e.target.value);
          for (let i = 0; i < vm.options_for_offences.length; i++) {
            if (vm.options_for_offences[i].id == offence_id) {
              // Update current offence
              vm.sanction_outcome.current_offence = vm.options_for_offences[i];
              return;
            }
          }
          // User selected the empty line
          vm.sanction_outcome.current_offence = {};
        },
        offenderSelected: function(e) {
          let vm = this;
          let offender_id = parseInt(e.target.value);
          for ( let i = 0; i < vm.sanction_outcome.current_offence.offenders.length; i++) {
            if ( vm.sanction_outcome.current_offence.offenders[i].id == offender_id) {
              // Update current offender
              vm.sanction_outcome.current_offender =
                vm.sanction_outcome.current_offence.offenders[i];
              return;
            }
          }
          // User selected the empty line
          vm.sanction_outcome.current_offender = {};
        },
        constructRegionsAndDistricts: async function() {
          let returned_regions = await cache_helper.getSetCacheList(
            "Regions",
            "/api/regions/"
        );
          Object.assign(this.regions, returned_regions);
          // blank entry allows user to clear selection
          this.regions.splice(0, 0, {
            id: "",
            name: "",
            district: "",
            districts: [],
            region: null
          });
          // regionDistricts
          // let returned_region_districts = await cache_helper.getSetCacheList(
          //   "RegionDistricts",
          //   api_endpoints.region_district
          // );
          // Object.assign(this.regionDistricts, returned_region_districts);
        },
        sendData: async function() {
            let vm = this;
            let alleged_offence_ids_included = [];
            let alleged_offence_ids_excluded = [];
            let checkboxes = $(".alleged_offence_include");
            for (let i = 0; i < checkboxes.length; i++) {
                if (checkboxes[i].checked) {
                    alleged_offence_ids_included.push(checkboxes[i].value);
                } else {
                    alleged_offence_ids_excluded.push(checkboxes[i].value);
                }
            }

            let postUrl = api_endpoints.sanction_outcome;

            let payload = new Object();
            Object.assign(payload, vm.sanction_outcome);
            if (payload.date_of_issue) {
                payload.date_of_issue = moment(payload.date_of_issue, "DD/MM/YYYY").format("YYYY-MM-DD");
                payload.time_of_issue = moment(payload.time_of_issue, 'LT').format('HH:mm');
            }
            payload.alleged_offence_ids_included = alleged_offence_ids_included;
            payload.alleged_offence_ids_excluded = alleged_offence_ids_excluded;
            // temporary doc
            //this.temporary_document_collection_id ? payload.temporary_document_collection_id = this.temporary_document_collection_id : null;
            //this.temporary_document_collection_id ? payload.append('temporary_document_collection_id', this.temporary_document_collection_id.temp_doc_id) : null;
            if (this.temporary_document_collection_id) {
                payload.temporary_document_collection_id = this.temporary_document_collection_id.temp_doc_id;
            } else {
                payload.temporary_document_collection_id = null;
            }

            // Retrieve remediation actions and set them to the payload
            let remediation_actions_rows = vm.$refs.tbl_remediation_actions.vmDataTable.rows() //.data().toArray();
            let remediation_actions_data = remediation_actions_rows.data()
            let remediation_actions = remediation_actions_data.toArray()
            payload.remediation_actions = remediation_actions;
            for (let i = 0; i < payload.remediation_actions.length; i++) {
                payload.remediation_actions[i].due_date = moment(payload.remediation_actions[i].due_date, "DD/MM/YYYY").format("YYYY-MM-DD");
            }

            payload.call_email_id = this.$parent.call_email ? this.$parent.call_email.id : null;
            payload.inspection_id = this.$parent.inspection ? this.$parent.inspection.id : null;
            payload.workflow_type = 'send_to_manager'  // Because this modal is used only when creating new sanction outcome to send to manager

            const savedObj = await Vue.http.post(postUrl, payload);
            return savedObj;
        },
        currentOffenderChanged: function() {
            console.log('*** currentOffenderChanged ***');
            this.constructAllegedOffencesTable();
        },
        clearTableAllegedOffence: function() {
          this.$refs.tbl_alleged_offence.vmDataTable.rows().remove().draw(); // Clear the table anyway
        },
        clearTableRemediationActions: function() {
          this.$refs.tbl_remediation_actions.vmDataTable.rows().remove().draw(); // Clear the table anyway
        },
        currentOffenceChanged: function() {
            this.sanction_outcome.current_offender = {};

            // The dropdown list of the offenders are directly linked to the vm.sanction_outcome.offence.offenders.
            // That's why the dropdown list is updated automatically whenever vm.sanction_outcome.offence is chanaged.
            this.constructAllegedOffencesTable();
        },
        constructAllegedOffencesTable: function(){
            console.log('*** constructAllegedOffencesTable ***');
            let current_offender_id = 0
            if (this.sanction_outcome.current_offender.person){
                current_offender_id = this.sanction_outcome.current_offender.person.id;
            }

            // Construct the datatable of the alleged offences
            this.clearTableAllegedOffence();

            if (this.sanction_outcome.current_offence && this.sanction_outcome.current_offence.alleged_offences) {
                for (let j = 0; j < this.sanction_outcome.current_offence.alleged_offences.length; j++) {
                    let alleged_offence = this.sanction_outcome.current_offence.alleged_offences[j];

                    // Check if this alleged offence has already connection to the current user
                    // Then store that info into the alleged_offence object, so that it can be used when render at mRender()
                    let connected = false
                    for (let i=0; i<alleged_offence.connected_offenders.length; i++){
                        if (alleged_offence.connected_offenders[i].id == current_offender_id){
                            connected = true
                        }
                    }
                    alleged_offence.connected = connected;

                    this.$refs.tbl_alleged_offence.vmDataTable.row.add(alleged_offence).draw();
                }
            }
        },
        updateOptionsForOffences: async function() {
            // This modal is used not onfly from an offence but also from the several entities, such as call_email, inspection, etc.
            let returned = null;
            if (this.$parent.call_email && this.$parent.call_email.id) {
                returned = await Vue.http.get("/api/offence/filter_by_call_email.json", {
                    params: { call_email_id: this.$parent.call_email.id }
                });
                this.options_for_offences = returned.body;
            } else if (this.$parent.inspection && this.$parent.inspection.id) {
                returned = await Vue.http.get("/api/offence/filter_by_inspection.json", {
                    params: { inspection_id: this.$parent.inspection.id }
                });
                this.options_for_offences = returned.body;
            } else if (this.$parent.offence && this.$parent.offence.id) {
                this.options_for_offences = [this.$parent.offence];
            } else if (this.$parent.legal_case && this.$parent.legal_case.id) {
                returned = await Vue.http.get("/api/offence/filter_by_legal_case.json", {
                    params: { legal_case_id: this.$parent.legal_case.id }
                });
                this.options_for_offences = returned.body;
            }
        },
        createDocumentActionUrl: async function() {
            // create sanction outcome and get id
            let returned_sanction_outcome = await Vue.http.post(api_endpoints.sanction_outcome);
            this.sanction_outcome.id = returned_sanction_outcome.body.id;

            return helpers.add_endpoint_join(
                api_endpoints.sanction_outcome,
                this.sanction_outcome.id + "/process_default_document/"
            )
        }
    },
    created: async function() {
        // Load all the types for the sanction outcome
        let options_for_types = await cache_helper.getSetCacheList(
            "SanctionOutcome_Types",
            "/api/sanction_outcome/types.json"
        );
        this.options_for_types.push({ id: "", display: "" });
        for (let i = 0; i < options_for_types.length; i++) {
            this.options_for_types.push(options_for_types[i]);
        }
        await this.updateOptionsForOffences();
        await this.constructRegionsAndDistricts();
        this.loadDefaultData();
    },
    mounted: function() {
        this.$nextTick(() => {
            this.addEventListeners();
            this.elem_paper_id_notice = $('#paper_id_notice');
            this.makeModalsDraggable();
        });
    }
};
</script>

<style lang="css" scoped>
.tab-content {
  background: white;
  padding: 10px;
  border: solid 1px lightgray;
}
</style>
