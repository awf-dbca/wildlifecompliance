<template lang="html">
    <div class="container-fluid">
        <div :class="componentClass">
            <div class="form-group">
                <div class="row">
                    <div v-if="!legalCaseExists">
                        <ul class="nav nav-pills">
                        </ul>
                    </div>
                    <div v-else>
                        <ul class="nav nav-pills">
                            <!--li class="nav-item active"><a data-toggle="tab" :href="'#'+newTab">New</a></li-->
                            <li class="nav-item active"><a data-toggle="tab" @click="updateTabSelected('objectTab')" :href="'#'+newTab">New</a></li>
                            <li class="nav-item"><a data-toggle="tab" :href="'#'+existingTab" >Existing</a></li>
                        </ul>
                    </div>
                    <div class="tab-content">
                        <div :id="newTab" class="tab-pane fade in active">
                            <ul class="nav nav-pills">
                                <li :class="objectTabListClass"><a data-toggle="tab" @click="updateTabSelected('objectTab')" :href="'#'+objectTab">Object</a></li>
                                <li :class="detailsTabListClass"><a data-toggle="tab" @click="updateTabSelected('detailsTab')" :href="'#'+detailsTab" >Details</a></li>
                                <li :class="storageTabListClass"><a data-toggle="tab" @click="updateTabSelected('storageTab')" :href="'#'+storageTab" >Storage</a></li>
                                <!--li v-if="disposalTabVisibility" :class="disposalTabListClass"><a data-toggle="tab" @click="updateTabSelected('disposalTab')" :href="'#'+disposalTab" >Disposal</a></li-->
                                <li :class="disposalTabListClass"><a data-toggle="tab" @click="updateTabSelected('disposalTab')" :href="'#'+disposalTab" >Disposal</a></li>
                                <li v-if="!parentModal" :class="relatedItemsTabListClass"><a data-toggle="tab" @click="updateTabSelected('relatedItemsTab')" :href="'#'+relatedItemsTab" >Related Items</a></li>
                            </ul>
                            <div class="tab-content">
                                <div :id="objectTab" :class="objectTabClass">
                                    <FormSection :formCollapse="false" :label="artifactTypeDisplay" Index="0" :hideHeader="!physicalArtifactIdExists">
                                        <div class="col-sm-12">
                                            <div class="form-group">
                                              <div class="row">
                                                <div class="col-sm-3">
                                                  <label>Physical Type</label>
                                                </div>
                                                <div class="col-sm-6">
                                                  <select :disabled="readonlyForm" class="form-control" v-model="physical_artifact.physical_artifact_type_id" @change="loadSchema">
                                                    <option  v-for="option in physicalArtifactTypes" :value="option.id" v-bind:key="option.id">
                                                      {{ option.artifact_type_display }}
                                                    </option>
                                                  </select>
                                                </div>
                                              </div>
                                            </div>
                                        </div>
                                        <div v-if="parentModal" class="col-sm-12 form-group"><div class="row">
                                          <label class="col-sm-6">Object used within this case?</label>
                                            <input :disabled="readonlyForm" class="col-sm-1" id="yes" type="radio" v-model="physical_artifact.used_within_case" v-bind:value="true">
                                            <label class="col-sm-1" for="yes">Yes</label>
                                            <input :disabled="readonlyForm" class="col-sm-1" id="no" type="radio" v-model="physical_artifact.used_within_case" v-bind:value="false">
                                            <label class="col-sm-1" for="no">No</label>
                                        </div></div>
                                        <div v-if="parentModal" class="col-sm-12 form-group"><div class="row">
                                          <label class="col-sm-6">Object is sensitive / non-disclosable?</label>
                                            <input :disabled="readonlyForm" class="col-sm-1" id="yes" type="radio" v-model="physical_artifact.sensitive_non_disclosable" v-bind:value="true">
                                            <label class="col-sm-1" for="yes">Yes</label>
                                            <input :disabled="readonlyForm" class="col-sm-1" id="no" type="radio" v-model="physical_artifact.sensitive_non_disclosable" v-bind:value="false">
                                            <label class="col-sm-1" for="no">No</label>
                                        </div></div>
                                        <div class="col-sm-12">
                                            <div class="form-group">
                                              <div class="row">
                                                <div class="col-sm-3">
                                                  <label>Identifier</label>
                                                </div>
                                                <div class="col-sm-9">
                                                  <input :readonly="readonlyForm" class="form-control" v-model="physical_artifact.identifier"/>
                                                </div>
                                              </div>
                                            </div>
                                            <div class="form-group">
                                                <div class="row">
                                                    <div class="col-sm-3">
                                                        <label>Officer</label>
                                                    </div>
                                                    <div class="col-sm-9">
                                                        <select 
                                                            id="physical_artifact_officers"  
                                                            name="physical_artifact_officers"  
                                                            ref="physical_artifact_officers" 
                                                            class="form-control" 
                                                        />
                                                        <!--select :disabled="readonlyForm" ref="physical_artifact_department_users" class="form-control" v-model="physical_artifact.officer_email">
                                                            <option  v-for="option in departmentStaffList" :value="option.email" v-bind:key="option.pk">
                                                            {{ option.name }}
                                                            </option>
                                                        </select-->
                                                    </div>
                                                </div>
                                            </div>
                                            <div v-if="statementVisibility" class="form-group">
                                              <div class="row">
                                                <div class="col-sm-3">
                                                  <label>Statement</label>
                                                </div>
                                                <div v-if="parentModal" class="col-sm-6">
                                                  <select :disabled="readonlyForm" class="form-control" v-model="physical_artifact.statement_id" ref="setStatement">
                                                    <option  v-for="option in legal_case.statement_artifacts" :value="option.id" v-bind:key="option.id">
                                                    {{ option.document_type_display }}: {{ option.identifier }}
                                                    </option>
                                                  </select>
                                                </div>
                                                <div v-else class="col-sm-6">
                                                  <select :disabled="readonlyForm" class="form-control" v-model="physical_artifact.statement_id" ref="setStatement">
                                                    <option  v-for="option in physical_artifact.available_statement_artifacts" :value="option.id" v-bind:key="option.id">
                                                    {{ option.document_type_display }}: {{ option.identifier }}
                                                    </option>
                                                  </select>
                                                </div>
                                              </div>
                                            </div>
                                            <div v-if="custodianVisibility" class="form-group">
                                                <div class="row">
                                                    <div class="col-sm-3">
                                                        <label>Custodian</label>
                                                    </div>
                                                    <div class="col-sm-9">
                                                            {{ selectedStatementArtifact.custodian }}
                                                    </div>
                                                </div>
                                            </div>
                                            <div v-else class="form-group">
                                                <div class="row">
                                                    <div class="col-sm-3">
                                                        <label>Custodian</label>
                                                    </div>
                                                    <div class="col-sm-9">
                                                        <select 
                                                            id="physical_artifact_custodians"  
                                                            name="physical_artifact_custodians"  
                                                            ref="physical_artifact_custodians" 
                                                            class="form-control" 
                                                        />
                                                        <!--select :disabled="readonlyForm" ref="physical_artifact_department_users_custodian" class="form-control" v-model="physical_artifact.custodian_email">
                                                            <option  v-for="option in departmentStaffList" :value="option.email" v-bind:key="option.pk">
                                                            {{ option.name }}
                                                            </option>
                                                        </select-->
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="form-group">
                                                <div class="row">
                                                    <label class="col-sm-3">Date</label>
                                                    <div class="col-sm-3">
                                                        <div class="input-group date" ref="artifactDatePicker">
                                                            <input :disabled="readonlyForm" type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="physical_artifact.artifact_date" />
                                                            <span class="input-group-addon">
                                                                <span class="glyphicon glyphicon-calendar"></span>
                                                            </span>
                                                        </div>
                                                    </div>
                                                    <label class="col-sm-3">Time</label>
                                                    <div class="col-sm-3">
                                                        <div class="input-group date" ref="artifactTimePicker">
                                                          <input :disabled="readonlyForm" type="text" class="form-control" placeholder="HH:MM" v-model="physical_artifact.artifact_time"/>
                                                          <span class="input-group-addon">
                                                              <span class="glyphicon glyphicon-calendar"></span>
                                                          </span>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="form-group">
                                              <div class="row">
                                                <div class="col-sm-3">
                                                  <label>Description</label>
                                                </div>
                                                <div class="col-sm-9">
                                                  <textarea :readonly="readonlyForm" class="form-control" v-model="physical_artifact.description"/>
                                                </div>
                                              </div>
                                            </div>
                                            <div v-if="siezureNoticeVisibility" class="form-group">
                                                <div class="row">
                                                    <div class="col-sm-3">
                                                        <label class="control-label pull-left" for="Name">Seizure Notice</label>
                                                    </div>
                                                    <div v-if="parentModal" class="col-sm-9">
                                                        <filefield
                                                        ref="default_document"
                                                        name="default_document"
                                                        :isRepeatable="true"
                                                        documentActionUrl="temporary_document"
                                                        :readonly="readonlyForm"
                                                        @update-temp-doc-coll-id="addToTemporaryDocumentCollectionList"/>
                                                    </div>
                                                    <div v-else class="col-sm-9">
                                                        <filefield 
                                                        ref="physical_artifact_documents" 
                                                        name="physical-artifact-documents" 
                                                        :isRepeatable="true" 
                                                        :documentActionUrl="physical_artifact.defaultDocumentUrl" 
                                                        :readonly="readonlyForm"
                                                        />
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </FormSection>
                                </div>
                                <!--div :id="detailsTab" class="tab-pane fade in li-top-buffer">
                                    details
                                </div>
                                <div :id="storageTab" class="tab-pane fade in li-top-buffer">
                                    storage
                                </div>
                                <div :id="disposalTab" class="tab-pane fade in li-top-buffer">
                                    disposal
                                </div-->
                                <div :id="detailsTab" :class="detailsTabClass" v-bind:key="artifactType">
                                    <FormSection :formCollapse="false" label="Details">
                                        <div class="col-sm-12 form-group"><div class="row">
                                            <div v-if="detailsSchemaVisibility" v-for="(item, index) in detailsSchema">
                                              <compliance-renderer-block
                                                 :component="item"
                                                 :readonlyForm="readonlyForm"
                                                 v-bind:key="`compliance_renderer_block${index}`"
                                                @update-temp-doc-coll-id="addToTemporaryDocumentCollectionList"
                                                />
                                            </div>
                                        </div></div>
                                    </FormSection>
                                </div>
                                <div :id="storageTab" :class="storageTabClass">
                                    <FormSection :formCollapse="false" label="Storage" v-bind:key="artifactType">
                                        <div class="col-sm-12 form-group"><div class="row">
                                            <div v-if="storageSchemaVisibility" v-for="(item, index) in storageSchema">
                                              <compliance-renderer-block
                                                 :component="item"
                                                 :readonlyForm="readonlyForm"
                                                 v-bind:key="`compliance_renderer_block${index}`"
                                                />
                                            </div>
                                        </div></div>
                                    </FormSection>
                                </div>
                                <!--div v-if="disposalTabVisibility" :id="disposalTab" :class="disposalTabClass"-->
                                <div :id="disposalTab" :class="disposalTabClass">
                                    <FormSection :formCollapse="false" label="Disposal">
                                        <div class="col-sm-12 form-group"><div class="row">
                                            <div class="col-sm-3">
                                              <label>Disposal Method</label>
                                            </div>
                                            <div class="col-sm-6">
                                              <select :disabled="readonlyForm" class="form-control" v-model="physical_artifact.disposal_method">
                                                <option  v-for="option in disposalMethods" :value="option" v-bind:key="option.id">
                                                  {{ option.disposal_method }}
                                                </option>
                                              </select>
                                            </div>
                                        </div></div>
                                        <div class="col-sm-12 form-group"><div class="row">
                                            <label class="col-sm-3">Date</label>
                                            <div class="col-sm-3">
                                                <div class="input-group date" ref="disposalDatePicker">
                                                    <input :disabled="readonlyForm" type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="physical_artifact.disposal_date" />
                                                    <span class="input-group-addon">
                                                        <span class="glyphicon glyphicon-calendar"></span>
                                                    </span>
                                                </div>
                                            </div>
                                        </div></div>
                                        <div class="col-sm-3">
                                          <label>Disposal details</label>
                                        </div>
                                        <div class="col-sm-9">
                                          <textarea :readonly="readonlyForm" class="form-control" v-model="physical_artifact.disposal_details"/>
                                        </div>
                                    </FormSection>
                                </div>
                                <div :id="relatedItemsTab" v-if="!parentModal" :class="relatedItemsTabClass">
                                    <FormSection :formCollapse="false" label="Related Items">
                                        <div class="col-sm-12 form-group"><div class="row">
                                            <div class="col-sm-12" v-if="relatedItemsVisibility">
                                                <RelatedItems
                                                :parent_update_related_items="setRelatedItems" 
                                                v-bind:key="relatedItemsBindId" 
                                                :readonlyForm="readonlyForm"
                                                parentComponentName="physical_artifact"
                                                />
                                            </div>
                                        </div></div>
                                    </FormSection>
                                </div>
                            </div>
                        </div>
                        <div v-if="parentModal" :id="existingTab" class="tab-pane fade in li-top-buffer">
                            <div class="row">
                                <div class="col-lg-12">
                                    <datatable ref="existing_artifact_table" id="existing-artifact-table" :dtOptions="dtOptions" :dtHeaders="dtHeaders" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>
<script>
import Vue from "vue";
//import modal from '@vue-utils/bootstrap-modal.vue';
import { mapState, mapGetters, mapActions, mapMutations } from "vuex";
import { api_endpoints, helpers, cache_helper } from "@/utils/hooks";
import filefield from '@/components/common/compliance_file.vue';
//import { required, minLength, between } from 'vuelidate/lib/validators'
//import 'bootstrap/dist/css/bootstrap.css';
//import 'eonasdan-bootstrap-datetimepicker';
import moment from 'moment';
import SearchPersonOrganisation from './search_person_or_organisation'
//require("select2/dist/css/select2.min.css");
//require("select2-bootstrap-theme/dist/select2-bootstrap.min.css");
import FormSection from "@/components/forms/section_toggle.vue";
import RelatedItems from "@common-components/related_items.vue";
import datatable from '@vue-utils/datatable.vue'

export default {
    name: "PhysicalArtifactComponent",
    data: function() {
        return {
            uuid: 0,
            relatedItemsTab: 'relatedItemsTab'+this._uid,
            newTab: 'newTab'+this._uid,
            existingTab: 'existingTab'+this._uid,
            objectTab: 'objectTab'+this._uid,
            detailsTab: 'detailsTab'+this._uid,
            storageTab: 'storageTab'+this._uid,
            disposalTab: 'disposalTab'+this._uid,
            tabSelected: 'objectTab',
            isModalOpen: false,
            processingDetails: false,
            documentActionUrl: '',
            //temporary_physical_collection_id: null,
            //temporary_physical_collection_list: [],
            physicalArtifactTypes: [],
            departmentStaffList: [],
            selectedCustodian: {},
            disposalMethods: [],
            detailsSchema: [],
            storageSchema: [],
            entity: {
                id: null,
            },
            statementArtifactTypes: [
                'record_of_interview',
                'witness_statement',
                'expert_statement',
                'officer_statement',
                ],
            statementVisibility: false,
            dtOptions: {
                serverSide: true,
                searchDelay: 1000,
                lengthMenu: [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],
                order: [
                    [0, 'desc']
                ],
                language: {
                    processing: "<i class='fa fa-4x fa-spinner fa-spin'></i>"
                },
                responsive: true,
                processing: true,
                ajax: {
                    url: '/api/artifact_paginated/get_paginated_datatable/?format=datatables',
                    dataSrc: 'data',
                    data: function(d) {
                        d.object_type = 'physical_artifact'
                        /*
                        d.type = vm.filterType;
                        d.status = vm.filterStatus;
                        d.date_from = vm.filterDateFromPicker;
                        d.date_to = vm.filterDateToPicker;
                        */
                    }
                },
                columns: [
                    {
                        data: 'number',
                        searchable: true,
                        orderable: true,
                    },
                    {
                        data: 'artifact_type',
                        searchable: true,
                        orderable: false,
                    },
                    {
                        data: 'identifier',
                        searchable: true,
                        orderable: true
                    },
                    {
                        searchable: false,
                        orderable: false,
                        data: 'digital_documents'
                    },
                    {
                        searchable: false,
                        orderable: false,
                        data: 'entity',
                        mRender: function (data, type,full){
                            let documentArtifactId = data.id;
                            let documentArtifactType = data.artifact_type ? data.artifact_type.replace(/\s/g, '~') : null;
                            let documentArtifactIdentifier = data.identifier ? data.identifier.replace(/\s/g, '~') : null;
                            return `<a data-id=${documentArtifactId} data-artifact-type=${documentArtifactType} data-data-type="document_artifact" data-identifier=${documentArtifactIdentifier} class="row_insert" href="#">Insert</a><br/>`
                            //return `<a class="row_insert" href="#">Insert</a><br/>`
                        }
                    }
                ],
            },
            dtHeaders: [
                'Number',
                'Document Type',
                'Identifier',
                /*
                'Date',
                'Custodian',
                'Status',
                */
                'Documents',
                'Action',
            ],

        }
    },
    components: {
      //modal,
      filefield,
      SearchPersonOrganisation,
      FormSection,
      RelatedItems,
      datatable,
    },
    props: {
        parentModal: {
            type: Boolean,
            required: false,
            default: false,
        },
        entityEdit: {
            type: Object,
            required: false,
        },
        readonlyForm: {
            type: Boolean,
            required: false,
            default: false,
        },
    },
    watch: {
        artifactType: {
            handler: function (newVal, oldVal){
                if (this.artifactType === 'found_object') {
                    this.setStatementId(null);
                }
                this.setStatementVisibility();
                /*
                if (this.statementVisibilityArray.includes(this.artifactType)) {
                    console.log("statementVisibility true")
                    this.statementVisibility = true;
                }
                */
            },
            //deep: true,
        },
        selectedStatementArtifact: {
            handler: function() {
            },
            deep: true,
        },
    },
    computed: {
        ...mapGetters('physicalArtifactStore', {
            physical_artifact: "physical_artifact",
        }),
        ...mapGetters('legalCaseStore', {
            legal_case: "legal_case",
        }),
        ...mapGetters({
            renderer_form_data: 'renderer_form_data'
        }),
        siezureNoticeVisibility: function() {
            let visibility = false;
            //console.log(this.artifactType)
            if (this.artifactType === 'seized_object') {
                visibility = true;
            }
            return visibility;
        },
        legalCaseExists: function() {
            let exists = false;
            if (this.legal_case && this.legal_case.id) {
                exists = true;
            }
            return exists;
        },
        componentClass: function() {
            let componentClass = '';
            if (this.parentModal) {
                componentClass = 'col-sm-11 child-artifact-component';
            }
            return componentClass;
        },
        selectedStatementArtifact: function() {
            let statementArtifact = {}
            if (this.physical_artifact && this.physical_artifact.statement_id) {
                if (this.parentModal && this.legal_case && this.legal_case.statement_artifacts) {
                    for (let artifact of this.legal_case.statement_artifacts) {
                        if (this.physical_artifact.statement_id === artifact.id) {
                            Object.assign(statementArtifact, artifact)
                        }
                    }
                } else if (!this.parentModal && this.physical_artifact.available_statement_artifacts) {
                    for (let artifact of this.physical_artifact.available_statement_artifacts) {
                        if (this.physical_artifact.statement_id === artifact.id) {
                            Object.assign(statementArtifact, artifact)
                        }
                    }
                }
            }
            return statementArtifact;
        },
        custodianVisibility: function() {
            let show = false;
            if (this.selectedStatementArtifact && this.selectedStatementArtifact.custodian) {
                show = true;
            }
            return show;
        },
        detailsSchemaVisibility: function() {
            console.log("detailsSchemaVisibility")
            if (this.artifactType && this.detailsSchema && this.detailsSchema.length > 0) {
                return true;
            } else {
                return false
            }
        },
        storageSchemaVisibility: function() {
            console.log("storageSchemaVisibility")
            if (this.artifactType && this.storageSchema && this.storageSchema.length > 0) {
                return true;
            } else {
                return false
            }
        },
        legalCaseId: function() {
          let ret_val = null;
          if (this.legal_case && this.legal_case.id) {
              ret_val = this.legal_case.id;
          }
          return ret_val;
        },
        /*
        legalCaseExists: function() {
          let caseExists = false;
          if (this.legal_case && this.legal_case.id) {
              caseExists = true;
          }
          return caseExists;
        },
        */
        linkedLegalCase: function() {
            let caseExists = false;
            if (this.physical_artifact && this.physical_artifact.legal_case_id_list && this.physical_artifact.legal_case_id_list.length > 0) {
                caseExists = true;
            }
            return caseExists;
        },
        canUserAction: function() {
            return true;
        },
        officerVisibility: function() {
            let visibility = true;
            /*
            let visibility = false;
            if (this.artifactType !== 'Expert Statement' && this.statementArtifactTypes.includes(this.artifactType)) {
                visibility = true;
            }
            */
            return visibility;
        },
        physicalArtifactId: function() {
            let id = null;
            if (this.physical_artifact && this.physical_artifact.id) {
                id = this.physical_artifact.id;
            }
            return id;
        },
        physicalArtifactIdExists: function() {
            let recordExists = false;
            if (this.physical_artifact && this.physical_artifact.id) {
                recordExists = true;
            }
            return recordExists;
        },
        artifactType: function() {
            let typeCode = ''
            if (this.artifactTypeId && this.physicalArtifactTypes && this.physicalArtifactTypes.length > 0) {
                for (let aType of this.physicalArtifactTypes) {
                    if (aType.id === this.artifactTypeId) {
                        typeCode = aType.artifact_type;
                    }
                }
            }
            return typeCode;
        },
        artifactTypeId: function() {
            let typeId = null
            if (this.physical_artifact) {
                typeId = this.physical_artifact.physical_artifact_type_id;
            }
            return typeId;
        },
        artifactTypeDisplay: function() {
            let display = '';
            if (this.artifactType) {
                for (let physicalArtifactType of this.physicalArtifactTypes) {
                    //if (this.artifactType && this.artifactType.id === this.artifactType) {
                    if (physicalArtifactType.artifact_type === this.artifactType) {
                        display = physicalArtifactType.artifact_type_display;
                    }
                }
            }
            return display;
        },
        /*
        readonlyForm: function() {
            let retValue = true;
            if (!this.readonly) {
                retValue = false;
            }
            return retValue;
        },
        */
        updateSearchPersonOrganisationBindId: function() {
            this.uuid += 1
            return "PhysicalArtifact_SearchPerson_" + this.uuid.toString();
        },
        objectTabSelected: function() {
            let isTab = false;
            if (this.tabSelected === 'objectTab') {
                isTab = true;
            }
            return isTab;
        },
        detailsTabSelected: function() {
            let isTab = false;
            if (this.tabSelected === 'detailsTab') {
                isTab = true;
            }
            return isTab;
        },
        storageTabSelected: function() {
            let isTab = false;
            if (this.tabSelected === 'storageTab') {
                isTab = true;
            }
            return isTab;
        },
        disposalTabSelected: function() {
            let isTab = false;
            if (this.tabSelected === 'disposalTab') {
                isTab = true;
            }
            return isTab;
        },
        relatedItemsTabSelected: function() {
            let isTab = false;
            if (this.tabSelected === 'relatedItemsTab') {
                isTab = true;
            }
            return isTab;
        },
        objectTabListClass: function() {
            let tabClass = 'nav-item';
            if (this.objectTabSelected) {
                tabClass += ' active';
            }
            return tabClass;
        },
        objectTabClass: function() {
            let tabClass = 'li-top-buffer tab-pane fade in';
            if (this.objectTabSelected) {
                tabClass += ' active';
            }
            return tabClass;
        },
        detailsTabListClass: function() {
            let tabClass = 'nav-item';
            if (this.detailsTabSelected) {
                tabClass += ' active';
            }
            return tabClass;
        },
        detailsTabClass: function() {
            let tabClass = 'li-top-buffer tab-pane fade in';
            if (this.detailsTabSelected) {
                tabClass += ' active';
            }
            return tabClass;
        },
        storageTabListClass: function() {
            let tabClass = 'nav-item';
            if (this.storageTabSelected) {
                tabClass += ' active';
            }
            return tabClass;
        },
        storageTabClass: function() {
            let tabClass = 'li-top-buffer tab-pane fade in';
            if (this.storageTabSelected) {
                tabClass += ' active';
            }
            return tabClass;
        },
        disposalTabListClass: function() {
            let tabClass = 'nav-item';
            if (this.disposalTabSelected) {
                tabClass += ' active';
            }
            return tabClass;
        },
        disposalTabClass: function() {
            let tabClass = 'li-top-buffer tab-pane fade in';
            if (this.disposalTabSelected) {
                tabClass += ' active';
            }
            return tabClass;
        },
        relatedItemsTabListClass: function() {
            let tabClass = 'nav-item';
            if (this.relatedItemsTabSelected) {
                tabClass += ' active';
            }
            return tabClass;
        },
        relatedItemsTabClass: function() {
            let tabClass = 'li-top-buffer tab-pane fade in';
            if (this.relatedItemsTabSelected) {
                tabClass += ' active';
            }
            return tabClass;
        },
        relatedItemsBindId: function() {
            let timeNow = Date.now()
            let bindId = null;
            if (this.physical_artifact && this.physical_artifact.id) {
                //bindId = 'physical_artifact_' + this.physical_artifact.id + '_' + this.uuid;
                bindId = 'physical_artifact_' + this.physical_artifact.id + '_' + timeNow.toString();
            } else {
                bindId = timeNow.toString();
            }
            return bindId;
        },
        relatedItemsVisibility: function() {
            let related_items_visibility = false;
            if (this.physical_artifact && this.physical_artifact.id) {
                related_items_visibility = true;
            }
            return related_items_visibility;
        },
        disposalTabVisibility: function() {
            let visibility = false;
            if (this.physical_artifact && this.physical_artifact.status === 'waiting_for_disposal') {
                visibility = true;
            }
            return visibility;
        },
    },
    filters: {
      formatDate: function(data) {
          return data ? moment(data).format("DD/MM/YYYY HH:mm:ss") : "";
      }
    },
    methods: {
        ...mapActions('physicalArtifactStore', {
            savePhysicalArtifact: 'savePhysicalArtifact',
            loadPhysicalArtifact: 'loadPhysicalArtifact',
            setPhysicalArtifact: 'setPhysicalArtifact',
            setRelatedItems: 'setRelatedItems',
            setOfficerId: 'setOfficerId',
            setCustodianId: 'setCustodianId',
            //setTemporaryDocumentCollectionId: 'setTemporaryDocumentCollectionId',
            addToTemporaryDocumentCollectionList: 'addToTemporaryDocumentCollectionList',
            setStatementId: 'setStatementId',
            setUsedWithinCase: 'setUsedWithinCase',
            setSensitiveNonDisclosable: 'setSensitiveNonDisclosable',
        }),
        setStatementVisibility: function() {
            if (
                // legal case exists and Document Type is not a statementArtifactType
                //(this.legalCaseExists && this.artifactType && !this.statementArtifactTypes.includes(this.artifactType)) ||
                ((this.linkedLegalCase || this.legalCaseExists) && this.artifactType &&
                    ['seized_object', 'surrendered_ object'].includes(this.artifactType)) ||
                //((this.linkedLegalCase || this.legalCaseExists)) ||
                // OR physical_artifact already has a linked statement
                (this.physical_artifact && this.physical_artifact.statement)
                )
            {
                //console.log("statementVisibility true")
                this.statementVisibility = true;
            } else {
                //console.log("statementVisibility false")
                this.statementVisibility = false;
            }
        },
        updateTabSelected: function(tabValue) {
            this.tabSelected = tabValue;
        },
        entitySelected: function(entity) {
            //console.log(entity);
            Object.assign(this.entity, entity)
        },
        save: async function() {
            if (this.physical_artifact.id) {
                await this.savePhysicalArtifact({ create: false, internal: false, legal_case_id: this.legalCaseId });
            } else {
                await this.savePhysicalArtifact({ create: true, internal: false, legal_case_id: this.legalCaseId });
                this.$nextTick(() => {
                    this.$emit('entity-selected', {
                        id: this.physical_artifact.id,
                        data_type: 'physical_artifact',
                        identifier: this.physical_artifact.identifier,
                        artifact_type: this.artifactType,
                        display: this.artifactType,
                    });
                });
            }
        },
        cancel: async function() {
            if (this.$refs.default_document) {
                await this.$refs.default_document.cancel();
            }
        },
        emitPhysicalArtifact: async function(e) {
            //console.log(e)
            let physicalArtifactId = e.target.dataset.id;
            // update existing DocumentArtifact with legal_case_id
            let fetchUrl = helpers.add_endpoint_join(
                api_endpoints.physical_artifact,
                physicalArtifactId + '/'
                )
            let payload = {
                "legal_case_id": this.legalCaseId
            }
            //console.log(payload);
            await Vue.http.put(fetchUrl, payload);
            let physicalArtifactType = e.target.dataset.artifactType.replace(/~/g, ' ');
            let physicalArtifactIdentifier = e.target.dataset.identifier.replace(/~/g, ' ').replace('null', '');
            this.$nextTick(() => {
                this.$emit('existing-entity-selected', {
                        id: physicalArtifactId,
                        data_type: 'physical_artifact',
                        identifier: physicalArtifactIdentifier,
                        artifact_type: physicalArtifactType,
                        display: physicalArtifactType,
                    });
            });
            //this.$parent.$parent.ok();
        },
        addEventListeners: function() {
            let vm = this;
            let el_fr_date = $(vm.$refs.artifactDatePicker);
            let el_fr_time = $(vm.$refs.artifactTimePicker);

            // "From" field
            el_fr_date.datetimepicker({
            format: "DD/MM/YYYY",
            maxDate: "now",
            showClear: true
            });
            el_fr_date.on("dp.change", function(e) {
                //console.log(e)
                if (el_fr_date.data("DateTimePicker").date()) {
                  vm.physical_artifact.artifact_date = e.date.format("DD/MM/YYYY");
                } else if (el_fr_date.data("date") === "") {
                  vm.physical_artifact.artifact_date = "";
                }
            });
            el_fr_time.datetimepicker({ format: "LT", showClear: true });
            el_fr_time.on("dp.change", function(e) {
                //console.log(e)
                if (el_fr_time.data("DateTimePicker").date()) {
                  vm.physical_artifact.artifact_time = e.date.format("LT");
                } else if (el_fr_time.data("date") === "") {
                  vm.physical_artifact.artifact_time = "";
                }
            });
            // department_users
            $(vm.$refs.physical_artifact_officers).select2({
                    minimumInputLength: 2,
                    "theme": "bootstrap",
                    allowClear: true,
                    placeholder:"",
                    ajax: {
                        url: api_endpoints.staff_member_lookup,
                        //url: api_endpoints.vessel_rego_nos,
                        dataType: 'json',
                        data: function(params) {
                            console.log(params)
                            var query = {
                                term: params.term,
                                type: 'public',
                            }
                            return query;
                        },
                    },
                }).
                on("select2:select",function (e) {
                    let selected = $(e.currentTarget);
                    let selectedData = selected.val();
                    console.log(selectedData);
                    vm.setOfficerId(selectedData);
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.setOfficerId(null);
                });
            // department_users_custodian
            $(vm.$refs.physical_artifact_custodians).select2({
                    "theme": "bootstrap",
                    allowClear: true,
                    placeholder:"",
                    minimumInputLength: 2,
                    ajax: {
                        url: api_endpoints.staff_member_lookup,
                        //url: api_endpoints.vessel_rego_nos,
                        dataType: 'json',
                        data: function(params) {
                            console.log(params)
                            var query = {
                                term: params.term,
                                type: 'public',
                            }
                            return query;
                        },
                    },
                }).
                on("select2:select",function (e) {
                    let selected = $(e.currentTarget);
                    let selectedData = selected.val();
                    vm.setCustodianId(selectedData);
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.setCustodianId(null);
                });

            let existingArtifactTable = $('#existing-artifact-table');
            existingArtifactTable.on(
                'click',
                '.row_insert',
                (e) => {
                    this.emitPhysicalArtifact(e);
                });

            //Disposal Date
            let disposal_date_control = $(vm.$refs.disposalDatePicker);
            // "From" field
            disposal_date_control.datetimepicker({
            format: "DD/MM/YYYY",
            maxDate: "now",
            showClear: true
            });
            disposal_date_control.on("dp.change", function(e) {
                //console.log(e)
                if (disposal_date_control.data("DateTimePicker").date()) {
                  vm.physical_artifact.disposal_date = e.date.format("DD/MM/YYYY");
                } else if (disposal_date_control.data("date") === "") {
                  vm.physical_artifact.disposal_date = "";
                }
            });
        },
        compare: function(a, b) {
            const nameA = a.name.toLowerCase();
            const nameB = b.name.toLowerCase();

            let comparison = 0;
            if (this.bandA > this.bandB) {
                comparison = 1;
            } else if (this.bandA < this.bandB) {
                comparison = -1;
            }
            return comparison;
        },
        loadSchema: async function() {
            this.$nextTick(async () => {
                if (this.artifactTypeId) {
                    console.log("really load schema")
                    let url = helpers.add_endpoint_json(
                                api_endpoints.physical_artifact_types,
                                this.artifactTypeId + '/get_schema',
                                );
                    let returnedSchema = await cache_helper.getSetCache(
                    'PhysicalArtifactTypeSchema',
                    this.artifactTypeId.toString(),
                    url);
                    if (returnedSchema) {
                        Object.assign(this.detailsSchema, returnedSchema.details_schema);
                        Object.assign(this.storageSchema, returnedSchema.storage_schema);

                    }
                } else {
                    console.log(" no artifactTypeId")
                }
            });
        },

    },
    mounted: function() {
      this.$nextTick(async () => {
          this.addEventListeners();
      });
    },
    beforeDestroy: async function() {
        //console.log("beforeDestroy")
        await this.setPhysicalArtifact({});
    },
    /*
    destroyed: function() {
        console.log("destroyed")
    },
    */
    created: async function() {
        console.log("created")
        if (this.$route.params.physical_artifact_id) {
            await this.loadPhysicalArtifact({ physical_artifact_id: this.$route.params.physical_artifact_id });
        } else if (this.entityEdit && this.entityEdit.id && this.entityEdit.data_type === 'physical_artifact') {
            await this.loadPhysicalArtifact({ physical_artifact_id: this.entityEdit.id });
            console.log("artifact loaded");
        }
        // load detailsSchema and storageSchema
        await this.loadSchema();
        this.setStatementVisibility();
        // physical artifact types
        let returned_physical_artifact_types = await cache_helper.getSetCacheList(
          'PhysicalArtifactTypes',
          api_endpoints.physical_artifact_types
          );
        Object.assign(this.physicalArtifactTypes, returned_physical_artifact_types);
        // blank entry allows user to clear selection
        this.physicalArtifactTypes.splice(0, 0,
          {
            id: "",
            artifact_type: "",
            description: "",
          });
        let returned_disposal_methods = await cache_helper.getSetCacheList(
          'DisposalMethods',
          api_endpoints.disposal_methods
          );
        Object.assign(this.disposalMethods, returned_disposal_methods);
        // blank entry allows user to clear selection
        this.disposalMethods.splice(0, 0,
          {
            id: "",
            disposal_method: "",
            description: "",
          });
        // Trigger Officer and Custodian select2 controls
        let vm=this;
        if (this.physical_artifact.officer && this.physical_artifact.officer.id) {
            console.log(this.physical_artifact.officer.id);
            var option = new Option(
                this.physical_artifact.officer.full_name, 
                this.physical_artifact.officer.full_name, 
                true, 
                true
            );
            $(vm.$refs.physical_artifact_officers).append(option).trigger('change');
        }
        if (this.physical_artifact.custodian && this.physical_artifact.custodian.id) {
            var option = new Option(
                this.physical_artifact.custodian.full_name, 
                this.physical_artifact.custodian.full_name, 
                true, 
                true
            );
            $(vm.$refs.physical_artifact_custodians).append(option).trigger('change');
        }

        this.$nextTick(async() => {
          // special processing for PhysicalArtifactLegalCases link
          if (this.legalCaseId && this.physical_artifact.legal_case_links && this.physical_artifact.legal_case_links.length > 0) {
              console.log("created links")
              for (let link of this.physical_artifact.legal_case_links) {
                  if (link.legal_case_id === this.legalCaseId) {
                      this.setUsedWithinCase(link.used_within_case);
                      this.setSensitiveNonDisclosable(link.sensitive_non_disclosable);
                  }
              }
          }
        });
    },
};
</script>

<style lang="css">
.child-artifact-component {
    margin-top: 20px;
    margin-left: 20px;
}
.li-top-buffer {
    margin-top: 20px;
}
.tab-content {
  background: white;
}
</style>
