<template lang="html">
    <div class="container-fluid">
        <div :class="componentClass">
<!--
            <div class="form-group">
                <div class="row">
-->
                    <div v-if="!legalCaseExists || !parentModal">
                        <ul class="nav nav-pills">
                            <li class="nav-item active"><a data-toggle="tab" :href="'#'+newTab">Object</a></li>
                            <li class="nav-item"><a data-toggle="tab" :href="'#'+rTab">Related Items</a></li>
                        </ul>
                    </div>
                    <div v-else>
                        <ul class="nav nav-pills">
                            <li class="nav-item active"><a data-toggle="tab" :href="'#'+newTab">New</a></li>
                            <li class="nav-item"><a data-toggle="tab" :href="'#'+existingTab" >Existing</a></li>
                        </ul>
                    </div>
                    <div class="tab-content">
                        <div :id="newTab" class="tab-pane fade in active">
                        <FormSection :formCollapse="false" :label="artifactTypeDisplay" Index="0" :hideHeader="!documentArtifactIdExists">
                            <div :id="objectTab" class="tab-pane fade in active li-top-buffer">
                                <div class="col-sm-12">
                                    <div class="form-group">
                                      <div class="row">
                                        <div class="col-sm-3">
                                          <label>Document Type</label>
                                        </div>
                                        <div class="col-sm-6">
                                          <select :disabled="readonlyForm" class="form-control" v-model="document_artifact.document_type" ref="setArtifactType">
                                            <option  v-for="option in documentArtifactTypes" :value="option.id" v-bind:key="option.id">
                                              {{ option.display }}
                                            </option>
                                          </select>
                                        </div>
                                      </div>
                                    </div>
                                </div>
                                <div class="col-sm-12">
                                    <div class="form-group">
                                        <div class="row">
                                            <div class="col-sm-3">
                                                <label class="control-label pull-left" for="Name">Document</label>
                                            </div>
                                            <div v-if="!documentArtifactId" class="col-sm-9">
                                                <filefield
                                                ref="default_document"
                                                name="default-document"
                                                :isRepeatable="true"
                                                documentActionUrl="temporary_document"
                                                @update-temp-doc-coll-id="setTemporaryDocumentCollectionId"/>
                                            </div>
                                            <div v-else class="col-sm-9">
                                                <filefield 
                                                ref="document_artifact_documents" 
                                                name="document-artifact-documents" 
                                                :isRepeatable="true" 
                                                :documentActionUrl="document_artifact.defaultDocumentUrl" 
                                                :readonly="readonlyForm"
                                                v-bind:key="documentArtifactId"
                                                />
                                            </div>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                      <div class="row">
                                        <div class="col-sm-3">
                                          <label>Identifier</label>
                                        </div>
                                        <div class="col-sm-9">
                                          <input :readonly="readonlyForm" class="form-control" v-model="document_artifact.identifier"/>
                                        </div>
                                      </div>
                                    </div>
                                    <div v-if="statementVisibility" class="form-group">
                                      <div class="row">
                                        <div class="col-sm-3">
                                          <label>Statement</label>
                                        </div>
                                        <div v-if="parentModal" class="col-sm-6">
                                          <select :disabled="readonlyForm" class="form-control" v-model="document_artifact.statement_id" ref="setStatement">
                                            <option  v-for="option in legal_case.statement_artifacts" :value="option.id" v-bind:key="option.id">
                                            {{ option.document_type_display }}: {{ option.identifier }}
                                            </option>
                                          </select>
                                        </div>
                                        <div v-else class="col-sm-6">
                                          <select :disabled="readonlyForm" class="form-control" v-model="document_artifact.statement_id" ref="setStatement">
                                            <option  v-for="option in document_artifact.available_statement_artifacts" :value="option.id" v-bind:key="option.id">
                                            {{ option.document_type_display }}: {{ option.identifier }}
                                            </option>
                                          </select>
                                        </div>
                                      </div>
                                    </div>
                                    <div v-if="offenceVisibility" class="form-group">
                                      <div class="row">
                                        <div class="col-sm-3">
                                          <label>Offence</label>
                                        </div>
                                        <div class="col-sm-6">
                                          <select :disabled="readonlyForm" class="form-control" v-model="document_artifact.offence_id" @change.prevent="setOffenderId(null)">
                                            <option  v-for="option in legal_case.offence_list" :value="option.id" v-bind:key="option.id">
                                                <div v-if="option.id">
                                                    {{ option.lodgement_number }}: {{ option.identifier }}
                                                </div>
                                            </option>
                                          </select>
                                        </div>
                                      </div>
                                    </div>
                                    <div v-if="offenceVisibility" class="form-group">
                                      <div class="row">
                                        <div class="col-sm-3">
                                          <label>Offender</label>
                                        </div>
                                        <div class="col-sm-6">
                                          <select :disabled="readonlyForm" class="form-control" v-model="document_artifact.offender_id">
                                            <option  v-for="option in offenderList" :value="option.offender_id" v-bind:key="option.offender_id">
                                            <div v-if="option.id">
                                                {{ option.full_name }}: {{ option.email }}
                                            </div>
                                            </option>
                                          </select>
                                        </div>
                                      </div>
                                    </div>
                                    <div class="form-group">
                                      <div class="row">
                                        <div class="col-sm-3">
                                          <label>Description</label>
                                        </div>
                                        <div class="col-sm-9">
                                          <textarea :readonly="readonlyForm" class="form-control" v-model="document_artifact.description"/>
                                        </div>
                                      </div>
                                    </div>
                                    <div v-if="personProvidingStatementVisibility" class="form-group">
                                        <div class="row">
                                            <div class="col-sm-3">
                                                <label>{{ personProvidingStatementLabel }}</label>
                                            </div>
                                            <div class="col-sm-9">
                                                <SearchPersonOrganisation 
                                                :parentEntity="personProvidingStatementEntity"
                                                personOnly
                                                :isEditable="!readonlyForm" 
                                                classNames="form-control" 
                                                @entity-selected="setPersonProvidingStatement"
                                                showCreateUpdate
                                                ref="document_artifact_search_person_organisation"
                                                v-bind:key="updateSearchPersonOrganisationBindId"
                                                addFullName
                                                :displayTitle="false"
                                                domIdHelper="document_artifact"
                                                departmentalStaff
                                                />
                                            </div>
                                        </div>
                                    </div>
                                    <div v-show="interviewerVisibility" class="form-group">
                                        <div class="row">
                                            <div class="col-sm-3">
                                                <label >{{ interviewerLabel }}</label>
                                            </div>
                                            <div class="col-sm-9">
                                                <!--select :disabled="readonlyForm" ref="document_artifact_department_users" class="form-control" v-model="officerInterviewerEmailAddress">
                                                    <option  v-for="option in departmentStaffList" :value="option.email" v-bind:key="option.pk">
                                                    {{ option.name }} 
                                                    </option>
                                                </select-->
                                                <select 
                                                    id="document_artifact_interviewer"  
                                                    name="document_artifact_interviewer"  
                                                    ref="document_artifact_interviewer" 
                                                    class="form-control" 
                                                />
                                            </div>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <div class="row">
                                            <label class="col-sm-3">Date</label>
                                            <div class="col-sm-3">
                                                <div class="input-group date" ref="artifactDatePicker">
                                                    <input :disabled="readonlyForm" type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="document_artifact.artifact_date" />
                                                    <span class="input-group-addon">
                                                        <span class="glyphicon glyphicon-calendar"></span>
                                                    </span>
                                                </div>
                                            </div>
                                            <label class="col-sm-3">Time</label>
                                            <div class="col-sm-3">
                                                <div class="input-group date" ref="artifactTimePicker">
                                                  <input :disabled="readonlyForm" type="text" class="form-control" placeholder="HH:MM" v-model="document_artifact.artifact_time"/>
                                                  <span class="input-group-addon">
                                                      <span class="glyphicon glyphicon-calendar"></span>
                                                  </span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </FormSection>
                        </div>
                        <div v-if="parentModal" :id="existingTab" class="tab-pane fade in li-top-buffer">
                            <div class="row">
                                <div class="col-lg-12">
                                    <datatable ref="existing_artifact_table" id="existing-artifact-table" :dtOptions="dtOptions" :dtHeaders="dtHeaders" />
                                </div>
                            </div>
                        </div>
                        <div v-if="!parentModal" :id="rTab" class="tab-pane fade in">
                            <FormSection :formCollapse="false" label="Related Items">
                                <div class="col-sm-12 form-group"><div class="row">
                                    <div class="col-sm-12" v-if="relatedItemsVisibility">
                                        <RelatedItems 
                                        :parent_update_related_items="setRelatedItems" 
                                        v-bind:key="relatedItemsBindId" 
                                        :readonlyForm="readonlyForm"
                                        parentComponentName="document_artifact"
                                        />
                                    </div>
                                </div></div>
                            </FormSection>
                        </div>
                    </div>
<!--
                </div>
            </div>
-->
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
import FormSection from "@/components/forms/section_toggle.vue";
import RelatedItems from "@common-components/related_items.vue";
import datatable from '@vue-utils/datatable.vue'

export default {
    name: "DocumentArtifactComponent",
    data: function() {
        return {
            uuid: 0,
            newTab: 'newTab'+this._uid,
            existingTab: 'existingTab'+this._uid,
            objectTab: 'objectTab'+this._uid,
            detailsTab: 'detailsTab'+this._uid,
            storageTab: 'storageTab'+this._uid,
            disposalTab: 'disposalTab'+this._uid,
            rTab: 'rTab'+this._uid,
            isModalOpen: false,
            processingDetails: false,
            documentActionUrl: '',
            temporary_document_collection_id: null,
            documentArtifactTypes: [],
            departmentStaffList: [],
            selectedDepartmentStaffMember: {},
            //offenderList: [],
            selectedCustodian: {},
            entity: {
                id: null,
            },
            /*
            statementArtifactTypes: [
                'Record of Interview',
                'Witness Statement',
                'Expert Statement',
                'Officer Statement',
                ],
                */
            statementArtifactTypes: [
                'record_of_interview',
                'witness_statement',
                'expert_statement',
                'officer_statement',
                ],
            statementVisibility: false,
            //departmentStaffList: [],
            //personProvidingStatementLabel: '',
            //interviewerLabel: '',
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
                        d.object_type = 'document_artifact'
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
                    /*
                    {
                        data: 'artifact_date',
                        searchable: false,
                        orderable: true,
                        mRender: function (data, type, full) {
                            return data != '' && data != null ? moment(data).format('DD/MM/YYYY') : '';
                        }
                    },
                    {
                        searchable: false,
                        orderable: false,
                        mRender: function (data, type,full){
                            return '---';
                        }
                    },
                    {
                        searchable: false,
                        orderable: false,
                        data: 'status'
                    },
                    */
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
        },
    },
    watch: {
        artifactType: {
            handler: function (){
                this.setStatementVisibility();
                //this.setPersonProvidingStatementLabel();
                //this.setInterviewerLabel();
                /*
                if (
                    // legal case exists and Document Type is not a statementArtifactType
                    (this.legalCaseExists && this.artifactType && !this.statementArtifactTypes.includes(this.artifactType)) ||
                    // OR document_artifact already has a linked statement
                    (this.document_artifact && this.document_artifact.statement)
                    )
                {
                    console.log("statementVisibility true")
                    this.statementVisibility = true;
                } else {
                    console.log("statementVisibility false")
                    this.statementVisibility = false;
                }
                */
            },
            deep: true,
        },
        /*
        legalCaseId: {
            handler: async function() {
                if (this.legal_case && this.legal_case.id) {
                    await this.setDocumentArtifactLegalId(this.legal_case.id)
                }
            },
        },
        */

    },
    computed: {
        ...mapGetters('documentArtifactStore', {
            document_artifact: "document_artifact",
        }),
        ...mapGetters('legalCaseStore', {
            legal_case: "legal_case",
        }),
        /*
        canUserAction: function() {
            return true;
        },
        */
        componentClass: function() {
            let componentClass = '';
            if (this.parentModal) {
                componentClass = 'col-sm-12 child-artifact-component';
            }
            return componentClass;
        },
        /*
        readonlyForm: function() {
            let retValue = false;
            if (!this.readonly) {
                retValue = true;
            }
            return retValue;
        },
        legalCaseExists: function() {
            let exists = false;
            if (this.legal_case && this.legal_case.id) {
                exists = true;
            }
            return exists;
        },
        */
        offenderList: function() {
            let offenderList = [{ 
                "id": null,
                "full_name": null,
                "email": null,
            }];
            //let offenderList = [];
            if (this.legalCaseExists && this.document_artifact.offence_id) {
                for (let offence of this.legal_case.offence_list) {
                    if (this.document_artifact.offence_id === offence.id) {
                        for (let offender of offence.offenders) {
                            let offenderObj = Object.assign({}, offender.person)
                            offenderObj.offender_id = offender.id
                            offenderList.push(offenderObj)
                        }
                    }
                }
            }
            return offenderList;
        },
        personProvidingStatementEntity: function() {
            let entity = {}
            if (this.document_artifact && this.document_artifact.person_providing_statement) {
                entity.id = this.document_artifact.person_providing_statement.id;
                entity.data_type = 'individual';
            }
            return entity;
        },
        legalCaseId: function() {
          let ret_val = null;
          if (this.legal_case && this.legal_case.id) {
              ret_val = this.legal_case.id;
          }
          return ret_val;
        },
        legalCaseExists: function() {
          let caseExists = false;
          if (this.legal_case && this.legal_case.id) {
              caseExists = true;
          }
          return caseExists;
        },
        linkedLegalCase: function() {
            let caseExists = false;
            if (this.document_artifact && this.document_artifact.legal_case_id_list && this.document_artifact.legal_case_id_list.length > 0) {
                caseExists = true;
            }
            return caseExists;
        },
        documentArtifactId: function() {
          let id = null;
          if (this.document_artifact && this.document_artifact.id) {
              id = this.document_artifact.id;
          }
          return id;
        },
        officerInterviewerEmailAddress: function() {
          let emailAddress = null;
          if (this.document_artifact && this.document_artifact.officer_interviewer) {
          //if (this.selectedDepartmentStaffMember) {
              emailAddress = this.document_artifact.officer_interviewer.email;
              //emailAddress = this.selectedDepartmentStaffMember.email;
          }
          return emailAddress;
        },
        documentArtifactIdExists: function() {
          let recordExists = false;
          if (this.document_artifact && this.document_artifact.id) {
              recordExists = true;
          }
          return recordExists;
        },
        /*
        artifactType: function() {
          console.log("artifact type")
          let aType = ''
          if (this.document_artifact && this.document_artifact.document_type) {
              aType = this.document_artifact.document_type.artifact_type;
          }
          return aType;
        },
        */
        artifactType: function() {
          console.log("artifact type")
          let aType = ''
          if (this.document_artifact) {
              aType = this.document_artifact.document_type;
          }
          return aType;
        },
        artifactTypeDisplay: function() {
            let display = '';
            if (this.artifactType) {
                for (let documentArtifactType of this.documentArtifactTypes) {
                    //if (this.artifactType && this.artifactType.id === this.artifactType) {
                    if (documentArtifactType.id === this.artifactType) {
                        display = documentArtifactType.display;
                    }
                }
            }
            return display;
        },
        offenceExists: function() {
            let oExists = false;
            if (this.document_artifact && this.document_artifact.offence) {
                oExists = true;
            }
            return oExists;
        },
        offenceVisibility: function() {
            let visibility = false;
            if ((this.legalCaseExists || this.offenceExists) && this.artifactType === 'record_of_interview') {
                visibility = true;
            }
            return visibility;
        },
        existingOffenceDisplay: function() {
            let display = '';
            if (this.offenceExists) {
                display = this.document_artifact.offence.lodgement_number + ": " + this.document_artifact.offence.identifier;
            }
            return display;
        },
        existingOffenderDisplay: function() {
            let display = '';
            if (this.offenceExists && this.document_artifact.offender && this.document_artifact.offender.person) {
                display = this.document_artifact.offender.person.full_name + ": " + this.document_artifact.offender.person.email;
            }
            return display;
        },
        personProvidingStatementLabel: function() {
            let label = '';
            if (this.artifactType === 'witness_statement') {
                label = 'Witness';
            } else if (this.artifactType === 'expert_statement') {
                label = 'Expert';
            }
            return label;
        },
        interviewerLabel: function() {
            let label = '';
            if (this.artifactType === 'witness_statement') {
                label = 'Officer taking statement'
            } else if (this.artifactType === 'record_of_interview') {
                label = 'Interviewer';
            } else if (this.artifactType === 'officer_statement') {
                label = 'Officer';
            }
            return label
        },
        personProvidingStatementVisibility: function() {
            let visibility = false;
            if (this.artifactType === 'expert_statement' || this.artifactType === 'witness_statement') {
                visibility = true;
            }
            return visibility;
        },
        interviewerVisibility: function() {
            let visibility = false;
            if (this.artifactType !== 'expert_statement' && this.statementArtifactTypes.includes(this.artifactType)) {
                visibility = true;
            }
            return visibility;
        },
        updateSearchPersonOrganisationBindId: function() {
          this.uuid += 1
          return "DocumentArtifact_SearchPerson_" + this.uuid.toString();
        },
        relatedItemsBindId: function() {
            let timeNow = Date.now()
            let bindId = null;
            if (this.document_artifact && this.document_artifact.id) {
                //bindId = 'document_artifact_' + this.document_artifact.id + '_' + this.uuid;
                bindId = 'document_artifact_' + this.document_artifact.id + '_' + timeNow.toString();
            } else {
                bindId = timeNow.toString();
            }
            return bindId;
        },
        relatedItemsVisibility: function() {
            let related_items_visibility = false;
            if (this.document_artifact && this.document_artifact.id) {
                related_items_visibility = true;
            }
            return related_items_visibility;
        },
    },
    filters: {
      formatDate: function(data) {
          return data ? moment(data).format("DD/MM/YYYY HH:mm:ss") : "";
      }
    },
    methods: {
        ...mapActions('documentArtifactStore', {
            saveDocumentArtifact: 'saveDocumentArtifact',
            loadDocumentArtifact: 'loadDocumentArtifact',
            setDocumentArtifact: 'setDocumentArtifact',
            setRelatedItems: 'setRelatedItems',
            setPersonProvidingStatementId: 'setPersonProvidingStatementId',
            setInterviewerId: 'setInterviewerId',
            setInterviewerEmail: 'setInterviewerEmail',
            setTemporaryDocumentCollectionId: 'setTemporaryDocumentCollectionId',
            //setDocumentArtifactLegalId: 'setDocumentArtifactLegalId',
            setOffenderId: 'setOffenderId',
            setOfficerInterviewer: 'setOfficerInterviewer',
            setOfficerInterviewerId: 'setOfficerInterviewerId',
        }),
        ...mapActions('legalCaseStore', {
            loadLegalCase: 'loadLegalCase',
        }),
        /*
        setOffenderList: function() {
            this.setOffenderId(null);
            this.$nextTick(() => {
                let oList = [{ 
                    "id": null,
                    "full_name": null,
                    "email": null,
                }];
                //let offenderList = [];
                if (this.legalCaseExists && this.document_artifact.offence_id) {
                    for (let offence of this.legal_case.offence_list) {
                        if (this.document_artifact.offence_id === offence.id) {
                            for (let offender of offence.offenders) {
                                oList.push(offender.person)
                            }
                        }
                    }
                }
                Object.assign(this.offenderList, oList);
            });
        },
        */
        setStatementVisibility: function() {
            if (
                // legal case exists and Document Type is not a statementArtifactType
                //(this.legalCaseExists && this.artifactType && !this.statementArtifactTypes.includes(this.artifactType)) ||
                ((this.linkedLegalCase || this.legalCaseExists) && this.artifactType && !this.statementArtifactTypes.includes(this.artifactType)) ||
                // OR document_artifact already has a linked statement
                (this.document_artifact && this.document_artifact.statement)
                )
            {
                console.log("statementVisibility true")
                this.statementVisibility = true;
            } else {
                console.log("statementVisibility false")
                this.statementVisibility = false;
            }
        },
        /*
        setTemporaryDocumentCollectionId: function(val) {
            this.temporary_document_collection_id = val;
        },
        */
        setPersonProvidingStatement: function(entity) {
            console.log(entity);
            //Object.assign(this.entity, entity)
            this.setPersonProvidingStatementId(entity.id);
        },
        save: async function() {
            if (this.document_artifact.id) {
                await this.saveDocumentArtifact({ create: false, internal: false, legal_case_id: this.legalCaseId });
            } else {
                await this.saveDocumentArtifact({ create: true, internal: false, legal_case_id: this.legalCaseId });
                this.$nextTick(() => {
                    this.$emit('entity-selected', {
                        id: this.document_artifact.id,
                        data_type: 'document_artifact',
                        identifier: this.document_artifact.identifier,
                        artifact_type: this.artifactType,
                        display: this.artifactType,
                    });
                });
            }
            console.log(this.document_artifact.error_message)
            this.$emit('error-message', {
                /*
                id: this.document_artifact.id,
                data_type: 'document_artifact',
                identifier: this.document_artifact.identifier,
                artifact_type: this.artifactType,
                display: this.artifactType,
                */
                error_message: this.document_artifact.error_message
            });
        },
        /*

        save: async function() {
            if (this.document_artifact.id) {
                await this.saveDocumentArtifact({ create: false, internal: false, legal_case_id: this.legalCaseId });
            } else {
                await this.saveDocumentArtifact({ create: true, internal: false, legal_case_id: this.legalCaseId });
            }
        },
        create: async function() {
            await this.saveDocumentArtifact({ create: true, internal: true, legal_case_id: this.legalCaseId });
            this.$nextTick(() => {
                this.$emit('entity-selected', {
                    id: this.document_artifact.id,
                    data_type: 'document_artifact',
                    identifier: this.document_artifact.identifier,
                    artifact_type: this.artifactType,
                    display: this.artifactTypeDisplay,
                });
            });
        },
        */
        cancel: async function() {
            if (this.$refs.default_document) {
                await this.$refs.default_document.cancel();
            }
        },
        emitDocumentArtifact: async function(e) {
            console.log(e)
            let documentArtifactId = e.target.dataset.id;
            // update existing DocumentArtifact with legal_case_id
            let fetchUrl = helpers.add_endpoint_join(
                api_endpoints.document_artifact,
                documentArtifactId + '/'
                )
            let payload = {
                "legal_case_id": this.legalCaseId
            }
            console.log(payload);
            await Vue.http.put(fetchUrl, payload);
            let documentArtifactType = e.target.dataset.artifactType.replace(/~/g, ' ');
            let documentArtifactIdentifier = e.target.dataset.identifier.replace(/~/g, ' ').replace('null', '');
            this.$nextTick(() => {
                this.$emit('existing-entity-selected', {
                        id: documentArtifactId,
                        data_type: 'document_artifact',
                        identifier: documentArtifactIdentifier,
                        artifact_type: documentArtifactType,
                        display: documentArtifactType,
                    });
            });
            //this.$parent.$parent.ok();
        },
        setOfficerInterviewerWrapper: async function(selectedData) {
            for (let officer of this.departmentStaffList) {
                if (officer.email === selectedData) {
                    //this.selectedDepartmentStaffMember = Object.assign({}, officer
                    this.selectedDepartmentStaffMember = officer
                }
            }
            await this.setOfficerInterviewer(this.selectedDepartmentStaffMember);
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
                console.log(e)
                if (el_fr_date.data("DateTimePicker").date()) {
                  vm.document_artifact.artifact_date = e.date.format("DD/MM/YYYY");
                } else if (el_fr_date.data("date") === "") {
                  vm.document_artifact.artifact_date = "";
                }
            });
            el_fr_time.datetimepicker({ format: "LT", showClear: true });
            el_fr_time.on("dp.change", function(e) {
                console.log(e)
                if (el_fr_time.data("DateTimePicker").date()) {
                  vm.document_artifact.artifact_time = e.date.format("LT");
                } else if (el_fr_time.data("date") === "") {
                  vm.document_artifact.artifact_time = "";
                }
            });
            /*
            // department_users
            $(vm.$refs.document_artifact_department_users).select2({
                    "theme": "bootstrap",
                    allowClear: true,
                    placeholder:""
                }).
                on("select2:select",function (e) {
                    console.log(e)
                    let selected = $(e.currentTarget);
                    let selectedData = selected.val();
                    console.log(selectedData)
                    vm.setOfficerInterviewerWrapper(selectedData);
                    //vm.setInterviewerEmail(selectedData);
                    //vm.setSelectedCustodian(selectedData);
                    //let custodianData = e.params.data
                    //console.log(custodianData)
                    //Object.assign(vm.selectedCustodian, custodianData);
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    vm.setInterviewerEmail('');
                    //vm.selectedCustodian = {}
                });
                */
            // department_users
            $(vm.$refs.document_artifact_interviewer).select2({
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
                    //vm.setOfficerInterviewerWrapper(selectedData);
                    vm.setOfficerInterviewerId(selectedData);
                }).
                on("select2:unselect",function (e) {
                    var selected = $(e.currentTarget);
                    //vm.setOfficerInterviewerWrapper(null);
                    vm.setOfficerInterviewerId(null);
                });

            let existingArtifactTable = $('#existing-artifact-table');
            existingArtifactTable.on(
                'click',
                '.row_insert',
                (e) => {
                    this.emitDocumentArtifact(e);
                    //console.log(e.target)
                    //this.$emit('entity-selected', {
                    //this.insertrunningSheetKeydown(e);
                });
            
            /*
            // artifact type events
            let artifactEvent = $(vm.$refs.setArtifactType);
            artifactEvent.on("change", function(e) {
            let artifactTypeId = e.target.value;
            });
            */
        },
        compare: function(a, b) {
            console.log("compare")
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

      //createDocumentActionUrl: async function(done) {
      //  if (!this.inspection.id) {
      //      // create inspection and update vuex
      //      let returned_inspection = await this.saveInspection({ create: true, internal: true })
      //      await this.loadInspection({inspection_id: returned_inspection.body.id});
      //  }
      //  // populate filefield document_action_url
      //  this.$refs.comms_log_file.document_action_url = this.inspection.createInspectionProcessCommsLogsDocumentUrl;
      //  return done(true);
      //},

    },
    mounted: function() {
      this.$nextTick(async () => {
          this.addEventListeners();
          /*
          if (this.legal_case && this.legal_case.id) {
              this.setDocumentArtifactLegalId(this.legal_case.id)
          */
      });
    },
    beforeDestroy: async function() {
        console.log("beforeDestroy")
        await this.setDocumentArtifact({});
    },
    created: async function() {
        console.log("created")
        if (this.$route.params.document_artifact_id) {
            await this.loadDocumentArtifact({ document_artifact_id: this.$route.params.document_artifact_id });
        } else if (this.entityEdit && this.entityEdit.id && this.entityEdit.data_type === 'document_artifact') {
            await this.loadDocumentArtifact({ document_artifact_id: this.entityEdit.id });
        }
        // if main obj page, call loadLegalCase if document_artifact.legal_case_id exists
        if (this.$route.name === 'view-artifact' && this.document_artifact && this.document_artifact.primary_legal_case_id) {
            await this.loadLegalCase({ legal_case_id: this.document_artifact.primary_legal_case_id });
        }
        this.setStatementVisibility();
        // document artifact types
        let returned_document_artifact_types = await cache_helper.getSetCacheList(
          'DocumentArtifactTypes',
          api_endpoints.document_artifact_types
          );
        Object.assign(this.documentArtifactTypes, returned_document_artifact_types);
        // blank entry allows user to clear selection
        this.documentArtifactTypes.splice(0, 0,
          {
            id: "",
            artifact_type: "",
            description: "",
          });
        // Trigger Officer Interviewer select2 controls
        let vm=this;
        if (this.document_artifact.officer_interviewer && this.document_artifact.officer_interviewer.id) {
            var option = new Option(
                this.document_artifact.officer_interviewer.full_name, 
                this.document_artifact.officer_interviewer.full_name, 
                true, 
                true
            );
            $(vm.$refs.document_artifact_interviewer).append(option).trigger('change');
        }

        /*
        // retrieve department_users from backend cache
        let returned_department_users = await this.$http.get(api_endpoints.department_users)
        Object.assign(this.departmentStaffList, returned_department_users.body)
        this.departmentStaffList.splice(0, 0,
          {
            pk: "",
            name: "",
          });
          */
    },
};
</script>

<style lang="css">
.child-artifact-component {
    margin-top: 20px;
}
.li-top-buffer {
    margin-top: 20px;
}
.tab-content {
  background: white;
}
</style>
