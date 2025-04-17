<template lang="html">
    <div>
            <FormSection :formCollapse="false" label="Court Dates">

                <div class="row file-upload-container">
                    <label class="col-md-3">Prosecution Notice</label>
                    <i style="color:red" class="fa fa-file-pdf-o col-md-1" id="prosecution-notice-icon"></i>
                    <label class="col-md-3">Attach signed file </label>
                    <div class="col-md-5">
                        <filefield ref="prosecution_notice_document"
                                   name="prosecution-notice-document"
                                   :documentActionUrl="legal_case.prosecutionNoticeDocumentUrl"
                                   @update-parent="courtOutcomeDocumentUploaded"
                                   :isRepeatable="false"
                                   :readonly="readonlyForm" />
                    </div>
                </div>
                <div class="row file-upload-container">
                    <label class="col-md-3">Court Hearing Notice</label>
                    <i style="color:red" class="fa fa-file-pdf-o col-md-1" id="court-hearing-notice-icon"></i>
                    <label class="col-md-3">Attach signed file </label>
                    <div class="col-md-5">
                        <filefield ref="court_hearing_notice_document"
                                   name="court-hearing-notice-document"
                                   :documentActionUrl="legal_case.courtHearingNoticeDocumentUrl"
                                   @update-parent="courtOutcomeDocumentUploaded"
                                   :isRepeatable="false"
                                   :readonly="readonlyForm" />
                    </div>
                </div>

                <div class="col-sm-12 form-group"><div class="row">
                    <template class="input-group date" id="court_date" v-for="court_date_obj in legal_case.court_proceedings.court_dates">
                        <template v-if="court_date_obj.court_datetime">
                            <CourtDate 
                                :court_datetime="new Date(court_date_obj.court_datetime)"
                                :comments="court_date_obj.comments"
                                :court="court_date_obj.court"
                                :court_date_id="court_date_obj.id"
                                :court_in_future="court_date_obj.court_in_future"
                                @data_changed="dataChanged"
                                :Key="court_date_obj.id"
                                />
                        </template>
                        <template v-else>
                            <CourtDate 
                                :comments="court_date_obj.comments"
                                :court="court_date_obj.court"
                                :court_date_id="court_date_obj.id"
                                :court_in_future="court_date_obj.court_in_future"
                                @data_changed="dataChanged"
                                :Key="court_date_obj.id"
                                />
                        </template>
                    </template>
                        <CourtDate 
                            @data_changed="dataChanged"
                            />

                </div></div>
            </FormSection>

            <FormSection :formCollapse="false" label="Court Journal">
                <div class="col-sm-12 form-group"><div class="row">
                    <div class="row action-button">
                        <div v-if="!readonlyForm">
                              <a @click="createNewCourtProceedingsEntry()" class="btn btn-primary pull-right new-row-button" >
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
                        ref="court_proceedings_table" 
                        id="court-proceedings-table" 
                        :dtOptions="dtOptionsCourtProceedings" 
                        :dtHeaders="dtHeadersCourtProceedings"
                        parentStyle=" "
                    />
                </div></div>
            </FormSection>

            <FormSection :formCollapse="false" label="Court Outcome">
                <template v-if="hasCourtProceedings">
                    <div class="row form-group" v-if="court_outcome_types.length > 0">
                        <label class="col-md-2">Type</label>
                        <div class="col-md-4">
                            <select 
                                :disabled="readonlyForm" 
                                class="form-control" 
                                v-model="legal_case.court_proceedings.court_outcome_type" 
                            >
                                <option value=""></option>
                                <option v-for="type in court_outcome_types" :value="type" :key="type.id">
                                    {{ type.identifier }}
                                </option>
                            </select>
                        </div>
                    </div>

                    <div class="row form-group">
                        <label class="col-md-2">Court outcome</label>
                        <div class="col-md-9">
                            <filefield ref="court_outcome_document"
                                       name="court-outcome-document"
                                       :documentActionUrl="legal_case.processCourtOutcomeDocumentUrl"
                                       @update-parent="courtOutcomeDocumentUploaded"
                                       :isRepeatable="true"
                                       :readonly="readonlyForm" />
                        </div>
                    </div>

                    <div class="row form-group">
                        <label class="col-md-2">Details</label>
                        <div class="col-md-9">
                            <textarea :readonly="readonlyForm" 
                                      class="form-control location_address_field" 
                                      v-model="legal_case.court_proceedings.court_outcome_details" />
                        </div>
                    </div>

                    <div class="row form-group">
                        <label class="col-md-2">Fines</label>
                        <div class="col-md-2">
                            <input :readonly="readonlyForm" 
                                   min="0"
                                   type="number"
                                   class="form-control currency" 
                                   v-model="legal_case.court_proceedings.court_outcome_fines" />
                        </div>
                    </div>

                    <div class="row form-group">
                        <label class="col-md-2">Costs</label>
                        <div class="col-md-2">
                            <input :readonly="readonlyForm" 
                                   min="0"
                                   type="number"
                                   class="form-control currency" 
                                   v-model="legal_case.court_proceedings.court_outcome_costs" />
                        </div>
                    </div>
                </template>
            </FormSection>
        <div v-if="courtProceedingsHistoryEntryBindId">
            <JournalHistory 
            ref="journal_history"
            :journalHistoryEntryInstance="journalHistoryEntryInstance"
            :key="courtProceedingsHistoryEntryBindId"
            />
        </div>
    </div>
</template>
<script>
import Vue from "vue";
import FormSection from "@/components/forms/section_toggle.vue";
import { api_endpoints, helpers, cache_helper } from "@/utils/hooks";
import utils from "@/components/external/utils";
import { mapState, mapGetters, mapActions, mapMutations } from "vuex";
import moment from 'moment';
import datatable from '@vue-utils/datatable.vue'
//import 'bootstrap/dist/css/bootstrap.css';
//import 'eonasdan-bootstrap-datetimepicker';
import _ from 'lodash';
import JournalHistory from './journal_history'
import filefield from '@/components/common/compliance_file.vue';
import CourtDate from '@/components/common/court_date'

export default {
    name: "ViewCourtProceedings",
    data: function() {
        return {
            uuid: 0,
            court_outcome_types: [],
            courtProceedingsEntriesUpdated: [],
            courtProceedingsEntriesUrl: [],
            courtProceedingsHistoryEntryBindId: '',
            journalHistoryEntryInstance: '',
            dtHeadersCourtProceedings: [
                "id",
                "Number",
                "Date",
                "Time",
                "User",
                "Description",
                "deleted",
                "Action",
            ],
            dtOptionsCourtProceedings: {
                order: [
                    [0, 'desc'],
                    ],
                columns: [
                    {
                        visible: false,
                        mRender: function(data, type, row) {
                            return row.id;
                        }
                    },
                    {
                        mRender: function(data, type, row) {
                            let retStr = row.number;
                            return retStr;
                        }
                    },
                    {
                        mRender: function(data, type, row) {
                            let retStr = row.date_mod;
                            return retStr;
                        }
                    },
                    {
                        mRender: function(data, type, row) {
                            let retStr = row.time_mod;
                            return retStr;
                        }
                    },
                    {
                        mRender: function(data, type, row) {
                            let retStr = row.user_full_name;
                            return retStr;
                        }
                    },
                    {
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
                        visible: false,
                        mRender: function(data, type, row) {
                            return row.deleted;
                        }
                    },
                    {
                        mRender: function(data, type, row) {
                            let retStr = '';
                            let rowIdDel = row.number.replace('-', 'D')
                            let rowIdHist = row.number.replace('-', 'H')
                            let rowIdReinstate = row.number.replace('-', 'R')
                            if (row.action) {
                                retStr += `<a id=${rowIdHist} class="row_history" href="#">History</a><br/><br/>`
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
        datatable,
        FormSection,
        JournalHistory,
        filefield,
        CourtDate,
    },
    computed: {
        ...mapGetters('legalCaseStore', {
            legal_case: "legal_case",
        }),
        readonlyForm: function() {
            let readonly = true
            if (this.legal_case && this.legal_case.id && !this.closedStatus) {
                readonly = !this.legal_case.can_user_action;
            }
            console.log('=== readonlyForm ===');
            console.log(readonly);
            return readonly
        },
        closedStatus: function() {
            let returnStatus = false
            if (this.legal_case && this.statusId === 'closed') {
                returnStatus = true
            }
            return returnStatus
        },
        statusId: function() {
            return this.legal_case.status ? this.legal_case.status.id : '';
        },
        ...mapGetters({
            current_user: 'current_user'
        }),

        csrf_token: function() {
            return helpers.getCookie("csrftoken");
        },
        canUserAction: function() {
            let return_val = false
            if (this.legal_case && this.legal_case.id) {
                return_val = this.legal_case.can_user_action;
            }
            return return_val
        },
        hasCourtProceedings: function() {
            return this.legal_case.court_proceedings ? true : false;
        },
    },
    filters: {
        formatDate: function(data) {
            return data ? moment(data).format("DD/MM/YYYY HH:mm:ss") : "";
        }
    },
    methods: {
        ...mapActions('legalCaseStore', {
            setCourtProceedingsJournalEntry: 'setCourtProceedingsJournalEntry',
            setAddCourtProceedingsEntry: 'setAddCourtProceedingsEntry',
            setCourtProceedingsTransform: 'setCourtProceedingsTransform',
            setCourtProceedingsDate: 'setCourtProceedingsDate',
        }),
        dataChanged: function(court_data_obj) {
            console.log('*** in dataChanged() ***');
            console.log(court_data_obj);
            try {
                if (court_data_obj.court_datetime.isValid()){
                    court_data_obj.court_datetime = court_data_obj.court_datetime.toDate().toISOString()
                } else {
                    court_data_obj.court_datetime = null;
                }
                this.setCourtProceedingsDate(court_data_obj);
            } catch (err) {

            }
        },
        courtOutcomeDocumentUploaded: function() {
            console.log('courtOutcomeDocumentUploaded');
        },
        setCourtProceedingsHistoryEntryBindId: function() {
            console.log('Inside setCourtProceedingsHistoryEntryBindId');
            if (this.journalHistoryEntryInstance) {
                this.uuid += 1;
                this.courtProceedingsHistoryEntryBindId = this.journalHistoryEntryInstance + '_' + this.uuid;
            }
        },
        generateDocument: async function(doc_type) {
            try {
                let payload = {};
                payload.document_type = doc_type;
                payload.court_date_id = ''
                if (this.legal_case.court_proceedings.court_dates.length > 0){
                    payload.court_date_id = this.legal_case.court_proceedings.court_dates[0].id
                }

                let post_url = '/api/legal_case/' + this.legal_case.id + '/generate_document/'
                const res = await fetch(
                    post_url, 
                    {
                        method: 'POST', 
                        body: JSON.stringify(payload),
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': this.csrf_token,
                        },
                    });
                console.log('generateDocument()');
                let buffer = await res.arrayBuffer();
                let file = new Blob([buffer], { type: 'application/pdf' });
                let fileURL = window.URL.createObjectURL(file);
                const elementId = 'generated-document-' + this.legal_case.id;
                let generatedDocument = document.createElement('a');
                generatedDocument.style.display = 'none';
                generatedDocument.href = fileURL;
                generatedDocument.download = payload.document_type + '_' + this.legal_case.number + '.pdf';
                document.body.appendChild(generatedDocument);
                generatedDocument.click();
                window.URL.revokeObjectURL(fileURL);
                return true
            } catch(err) {
                this.errorResponse = err.statusText;
            }
        },
        addEventListeners: function() {
            let vm = this;

            let prosecutionNoticeIcon = $('#prosecution-notice-icon');
            let courtHearingNoticeIcon = $('#court-hearing-notice-icon');
            let courtProceedingsTable = $('#court-proceedings-table');

            prosecutionNoticeIcon.on(
                'click',
                (e) => {
                    console.log(e);
                    this.generateDocument('prosecution_notice');
                }
            );
            courtHearingNoticeIcon.on(
                'click',
                (e) => {
                    console.log(e);
                    this.generateDocument('court_hearing_notice');
                }
            );

            courtProceedingsTable.on(
                'keyup',
                (e) => {
                    this.courtProceedingsKeyup(e)
                });
            courtProceedingsTable.on(
                'click',
                '.row_delete',
                (e) => {
                    this.courtProceedingsRowDelete(e)
                });
            courtProceedingsTable.on(
                'click',
                '.row_history',
                (e) => {
                    this.courtProceedingsRowHistory(e)
                });
            courtProceedingsTable.on(
                'click',
                '.row_reinstate',
                (e) => {
                    this.courtProceedingsRowReinstate(e)
                });
            courtProceedingsTable.on(
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
            this.preventDecimalPlaces();
        },
        preventDecimalPlaces: function() {
            $(".currency").change(function() {
                $(this).val(parseFloat($(this).val()).toFixed(2));
            });
        },
        courtProceedingsRowDelete: async function(e){
            this.showSpinner = true;
            let rowNumber = e.target.id.replace('D', '-');
            let journal_entry_id = null;
            for (let r of this.legal_case.court_proceedings.journal_entries) {
                if (r.number === rowNumber) {
                    journal_entry_id = r.id
                }
            }
            let returnedEntry = await Vue.http.post(
                helpers.add_endpoint_join(
                    api_endpoints.legal_case,
                    this.legal_case.id + '/delete_reinstate_journal_entry/',
                ),
                {
                    "journal_entry_id": journal_entry_id,
                    "deleted": true,
                }
            );
            if (returnedEntry.ok) {
                // required for running_sheet_history
                await this.setCourtProceedingsJournalEntry(returnedEntry.body);
                let i = 0;
                for (let r of this.courtProceedingsEntriesUrl) {
                    if (r.number === rowNumber) {
                        //this.courtProceedingsEntriesUrl.splice(i++, 1, returnedEntry.body);
                        //this.courtProceedingsEntriesUrl[i].description = this.tokenToUrl(this.runningSheetUrl[i].description);
                        //r = returnedEntry.body;
                        this.courtProceedingsEntriesUrl[i] = returnedEntry.body;
                    }
                    i++;
                }
                this.constructCourtProceedingsTableEntry(rowNumber);
            }
            this.showSpinner = false;
        },
        courtProceedingsRowHistory: function(e){
            console.log(e)
            let rowNumber = e.target.id.replace('H', '-');
            console.log(rowNumber)
            console.log("journalEntryRowHistory")
            this.journalHistoryEntryInstance = rowNumber;
            this.setCourtProceedingsHistoryEntryBindId()
            this.$nextTick(() => {
                this.$refs.journal_history.isModalOpen = true;
            });
        },
        courtProceedingsRowReinstate: async function(e){
            this.showSpinner = true;
            let rowNumber = e.target.id.replace('R', '-');
            let journal_entry_id = null;
            for (let r of this.legal_case.court_proceedings.journal_entries) {
                if (r.number === rowNumber) {
                    journal_entry_id = r.id
                }
            }
            let returnedEntry = await Vue.http.post(
                helpers.add_endpoint_join(
                    api_endpoints.legal_case,
                    this.legal_case.id + '/delete_reinstate_journal_entry/',
                ),
                {
                    "journal_entry_id": journal_entry_id,
                    "deleted": false,
                }
                );
            if (returnedEntry.ok) {
                // required for running_sheet_history
                await this.setCourtProceedingsJournalEntry(returnedEntry.body);
                let i = 0;
                for (let r of this.courtProceedingsEntriesUrl) {
                    if (r.number === rowNumber) {
                        console.log('update: ' + rowNumber);
                        //this.runningSheetUrl.splice(i, 1, returnedEntry.body);
                        //this.runningSheetUrl[i].description = this.tokenToUrl(this.runningSheetUrl[i].description);
                        this.courtProceedingsEntriesUrl[i] = returnedEntry.body;
                    }
                    i++;
                }
                this.constructCourtProceedingsTableEntry(rowNumber);
            }
            this.showSpinner = false;
        },
        courtProceedingsKeyup: function(e) {
            console.log('courtProceedingsKeyup');
            let rowObj = {}
            let recordNumber = e.target.id
            let recordDescriptionText = e.target.textContent
            let recordDescriptionHtml = e.target.innerHTML.replace(/\&nbsp\;/g, ' ');
            console.log('recordNumber: ' + recordNumber);
            console.log(recordDescriptionHtml);

            // add recordNumber to store rows updated
            if (!this.courtProceedingsEntriesUpdated.includes(recordNumber)) {
                this.courtProceedingsEntriesUpdated.push(recordNumber);
            }

        //    //const ignoreArray = [49, 50, 16]
        //    const ignoreArray = []
        //    if (ignoreArray.includes(e.which)) {
        //        //pass
        //    } else {
            for (let r of this.courtProceedingsEntriesUrl) {
                if (r.number === recordNumber) {
                    this.updateCourtProceedingsUrlEntry({
                        "recordNumber": recordNumber,
                        "recordDescription": recordDescriptionHtml, 
                        "redraw": false
                    })
                    console.log('r');
                    console.log(r);
                    this.setCourtProceedingsTransform(r);
                    //this.searchPersonKeyPressed = false;
                    //this.searchObjectKeyPressed = false;
                }
            }
        //    }
        },
        updateCourtProceedingsUrlEntry: function({ recordNumber, recordDescription, redraw }) {
            console.log("updateCourtProceedingsUrl")

            for (let r of this.courtProceedingsEntriesUrl) {
                if (r.number === recordNumber) {
                    r.description = recordDescription
                    if (redraw) {
                        this.constructCourtProceedingsTableEntry( recordNumber );
                    }
                }
            }
        },
        createNewCourtProceedingsEntry: async function() {
            console.log('aho');
            let payload = {
                "court_proceedings_id": this.legal_case.court_proceedings.id,
                "user_id": this.current_user.id,
            }
            let fetchUrl = helpers.add_endpoint_join(
                api_endpoints.legal_case,
                this.legal_case.id + '/create_journal_entry/'
                )
            let updatedCourtProceedings = await Vue.http.post(fetchUrl, payload);
            console.log(updatedCourtProceedings)
            if (updatedCourtProceedings.ok) {
                await this.setAddCourtProceedingsEntry(updatedCourtProceedings.body);
                let returnPayload = _.cloneDeep(updatedCourtProceedings.body);
                this.courtProceedingsEntriesUrl.push(returnPayload);
                this.constructCourtProceedingsTable(returnPayload.id);
            }
        },
        constructCourtProceedingsTableEntry: function( rowNumber ){
            console.log('rowNumber')
            console.log(rowNumber)

            let actionColumn = !this.readonlyForm;
            if (this.$refs.court_proceedings_table && this.$refs.court_proceedings_table.vmDataTable) {
                console.log("constructCourtProceedingsTableEntry");
                this.$refs.court_proceedings_table.vmDataTable.rows().every((rowIdx, tableLoop, rowLoop) => {
                    let rowData = this.$refs.court_proceedings_table.vmDataTable.row(rowIdx).data()
                    /*
                    console.log(rowIdx)
                    console.log(rowData)
                    */
                    if (rowData.number === rowNumber) {
                        let i = 0;
                        for (let r of this.courtProceedingsEntriesUrl) {
                            if (r.number === rowNumber) {
                                rowData.date_mod = this.courtProceedingsEntriesUrl[rowIdx].date_mod;
                                rowData.time_mod = this.courtProceedingsEntriesUrl[rowIdx].time_mod;
                                rowData.user_full_name = this.courtProceedingsEntriesUrl[rowIdx].user_full_name;
                                rowData.description = this.courtProceedingsEntriesUrl[rowIdx].description;
                                rowData.deleted = this.courtProceedingsEntriesUrl[rowIdx].deleted;
                                rowData.action = actionColumn;
                                this.$refs.court_proceedings_table.vmDataTable.row(rowIdx).invalidate().draw();
                            }
                            i += 1;
                        }
                    }
                });
            }
        },
        constructCourtProceedingsTableWrapper: function() {
            this.courtProceedingsEntriesUrl = _.cloneDeep(this.legal_case.court_proceedings.journal_entries);

            this.$nextTick(() => {
                this.constructCourtProceedingsTable();
            });
        },
        constructCourtProceedingsTable: function(pk){
            console.log("constructCourtProceedingsTable")

            if (this.hasCourtProceedings){
                if (!pk) {
                    this.$refs.court_proceedings_table.vmDataTable.clear().draw();
                }

                let actionColumn = !this.readonlyForm;
                //let entries = this.legal_case.court_proceedings.journal_entries;
                for(let i = 0;i < this.courtProceedingsEntriesUrl.length; i++){
                    if (!pk || this.courtProceedingsEntriesUrl[i].id === pk) {
                        this.$refs.court_proceedings_table.vmDataTable.row.add({ 
                            "id": this.courtProceedingsEntriesUrl[i].id,
                            "number": this.courtProceedingsEntriesUrl[i].number,
                            "date_mod": this.courtProceedingsEntriesUrl[i].date_mod,
                            "time_mod": this.courtProceedingsEntriesUrl[i].time_mod,
                            "user_full_name": this.courtProceedingsEntriesUrl[i].user_full_name,
                            "description": this.courtProceedingsEntriesUrl[i].description,
                            "deleted": this.courtProceedingsEntriesUrl[i].deleted,
                            "action": actionColumn,
                        }).draw();
                    }
                }
            }
            console.log("constructCourtProceedingsTable - end")
        },
        constructOptionsCourtOutcomeType: async function() {
            let returned= await cache_helper.getSetCacheList('CourtProceedings_CourtOutcomeTypes', '/api/legal_case/court_outcome_type_list');
            this.court_outcome_types = returned;
        },
    },
    created: async function() {
        this.constructOptionsCourtOutcomeType();
    },
    mounted: function() {
        this.$nextTick(() => {
            this.addEventListeners();
            $('.vue-treeselect__control').css("display", "none");
            this.constructCourtProceedingsTableWrapper();
        });
    },
};
</script>

<style lang="css">
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
.pdf-notices {
    display: flex;
    align-items: center;
}
.file-upload-container {
    margin-top: 1%;
    margin-bottom: 2%;
}
.currency {
    text-align: right;
}
</style>
