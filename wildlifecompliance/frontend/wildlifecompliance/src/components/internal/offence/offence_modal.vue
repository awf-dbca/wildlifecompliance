<template lang="html">
    <div>
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="modalTitle" large force>
            <div class="container-fluid">
                <ul class="nav nav-pills">
                    <li class="nav-item active"><a data-toggle="tab" :href="'#'+oTab">Offence</a></li>
                    <li class="nav-item"><a data-toggle="tab" :href="'#'+dTab">Details</a></li>
                    <li class="nav-item"><a data-toggle="tab" :href="'#'+documentTab">Document</a></li>
                    <li class="nav-item"><a data-toggle="tab" :href="'#'+pTab">Offender(s)</a></li>
                    <li class="nav-item"><a data-toggle="tab" :href="'#'+lTab" @click="mapOffenceClicked">Location</a></li>
                </ul>
                <div class="tab-content">
                    <div :id="oTab" class="tab-pane fade in active">
                        <div class="row">

                            <div class="col-sm-12 form-group"><div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left" for="offence-identifier">Identifier</label>
                                </div>
                                <div class="col-sm-6">
                                    <div v-if="offence">
                                        <input type="text" class="form-control" name="identifier" placeholder="" v-model="offence.identifier" v-bind:key="offence.id">
                                    </div>
                                </div>
                            </div></div>

                            <div class="col-sm-12 form-group"><div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left">Region</label>
                                </div>
                                <div class="col-sm-7">
                                  <select class="form-control col-sm-9" v-on:change.prevent="offence.region_id=$event.target.value; updateDistricts('updateFromUI')" v-bind:value="offence.region_id">
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
                                  <select class="form-control" v-model="offence.district_id">
                                    <option  v-for="option in availableDistricts" :value="option.district_id" v-bind:key="option.district_id">
                                      {{ option.district_name }} 
                                    </option>
                                  </select>
                                </div>
                            </div></div>

                            <div class="col-sm-12 form-group"><div class="row">
                                <label class="col-sm-3">Use occurrence from/to</label>
                                <input class="col-sm-1" id="occurrence_from_to_true" type="radio" v-model="offence.occurrence_from_to" v-bind:value="true">
                                <label class="col-sm-1 radio-button-label" for="occurrence_from_to_true">Yes</label>
                                <input class="col-sm-1" id="occurrence_from_to_false" type="radio" v-model="offence.occurrence_from_to" v-bind:value="false">
                                <label class="col-sm-1 radio-button-label" for="occurrence_from_to_false">No</label>
                            </div></div>

                            <div class="col-sm-12 form-group"><div class="row">
                                <label class="col-sm-3">{{ occurrenceDateLabel }}</label>
                                <div class="col-sm-3">
                                    <div class="input-group date" ref="occurrenceDateFromPicker">
                                        <input type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="offence.occurrence_date_from" />
                                        <span class="input-group-addon">
                                            <span class="glyphicon glyphicon-calendar"></span>
                                        </span>
                                    </div>
                                </div>
                                <label v-show="offence.occurrence_from_to" class="col-sm-1">to</label>
                                <div v-show="offence.occurrence_from_to">
                                    <div class="col-sm-3">
                                        <div class="input-group date" ref="occurrenceDateToPicker">
                                            <input type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="offence.occurrence_date_to" />
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
                                        <input type="text" class="form-control" placeholder="HH:MM" v-model="offence.occurrence_time_from" />
                                        <span class="input-group-addon">
                                            <span class="glyphicon glyphicon-calendar"></span>
                                        </span>
                                    </div>
                                </div>
                                <label v-show="offence.occurrence_from_to" class="col-sm-1">to</label>
                                <div v-show="offence.occurrence_from_to">
                                    <div class="col-sm-3">
                                        <div class="input-group date" ref="occurrenceTimeToPicker">
                                            <input type="text" class="form-control" placeholder="HH:MM" v-model="offence.occurrence_time_to" />
                                            <span class="input-group-addon">
                                                <span class="glyphicon glyphicon-calendar"></span>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div></div>

                            <div class="col-sm-12 form-group"><div class="row">
                                <label class="col-sm-3">Alleged Offence</label>
                                <div class="col-sm-6">
                                    <input class="form-control" id="alleged-offence" />
                                </div>
                                <div class="col-sm-3">
                                    <input type="button" class="btn btn-primary" value="Add" @click.prevent="addAllegedOffenceClicked()" />
                                </div>
                            </div></div>

                            <div class="col-sm-12 form-group"><div class="row">
                                <div class="col-sm-12">
                                    <datatable ref="alleged_offence_table" id="alleged-offence-table" :dtOptions="dtOptionsAllegedOffence" :dtHeaders="dtHeadersAllegedOffence" />
                                </div>
                            </div></div>
                        </div>
                    </div>

                    <div :id="dTab" class="tab-pane fade in">
                        <div class="row">
                            <div class="col-sm-12">
                                <div class="form-group">
                                    <div class="row">
                                        <div class="col-sm-3">
                                            <label class="control-label pull-left" for="offence-details">Details</label>
                                        </div>
                                        <div class="col-sm-6">
                                            <div v-if="offence">
                                                <textarea class="form-control" placeholder="add details" id="offence-details" v-model="offence.details" v-bind:key="offence.id"/>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div :id="documentTab" class="tab-pane face in">
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left"  for="Name">Attachments</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <FileField 
                                            ref="comms_log_file" 
                                            name="comms-log-file" 
                                            :isRepeatable="true" 
                                            documentActionUrl="temporary_document" 
                                            @update-temp-doc-coll-id="setTemporaryDocumentCollectionId"
                                        />
                                    </div>
                                </div>
                            </div>
                    </div>

                    <div :id="pTab" class="tab-pane fade in">
                        <div class="row"><div class="col-sm-12">

                            <!--div class="col-sm-12 form-group"><div class="row">
                                <input class="col-sm-1" id="offender_individual" type="radio" v-model="offender_search_type" value="individual">
                                <label class="col-sm-1 radio-button-label" for="offender_individual">Individual</label>
                                <input class="col-sm-1" id="offender_organisation" type="radio" v-model="offender_search_type" value="organisation">
                                <label class="col-sm-1 radio-button-label" for="offender_organisation">Organisation</label>
                            </div></div-->

                            <div class="form-group"><div class="row">
                                <div class="col-sm-12">
                                    <strong><label>Offender</label></strong>
                                </div>
                                <div>
                                    <SearchPersonOrganisation 
                                    :excludeStaff="true" 
                                    :personOnly="true" 
                                    classNames="form-control" 
                                    @entity-selected="personSelected" 
                                    showCreateUpdate
                                    ref="search_offender"
                                    domIdHelper="offender"
                                    :key="updateSearchPersonOrganisationBindId"/>
                                </div>
                            </div></div>

                            <div class="form-group"><div class="row">
                                <div class="col-sm-12">
                                    <input type="button" class="btn btn-primary" value="Add to Offender List" @click.prevent="addOffenderClicked()" />
                                </div>
                            </div></div>
                            <div class="form-group"><div class="row">

                                <div class="col-sm-12">
                                    <datatable ref="offender_table" id="offender-table" :dtOptions="dtOptionsOffender" :dtHeaders="dtHeadersOffender" />
                                </div>
                            </div></div>
                        </div></div>
                    </div>

                    <div :id="lTab" class="tab-pane fade in">
                        <div class="row">
                            <div class="col-sm-12 form-group">
                                <div v-if="offence.location">
                                    <MapLocationOffence v-bind:key="lTab" :id="lTab" ref="mapOffenceComponent"/>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div slot="footer">
                <div v-if="errorResponse" class="form-group">
                    <div class="row">
                        <div class="col-sm-12">
                            <strong>
                                <span style="white-space: pre;" v-html="errorResponse"></span>
                            </strong>
                        </div>
                    </div>
                </div>
                <button type="button" v-if="processingDetails" disabled class="btn btn-default" @click="ok"><i class="fa fa-spinner fa-spin"></i> Adding</button>
                <button type="button" v-else class="btn btn-default" @click="ok">Ok</button>
                <button type="button" class="btn btn-default" @click="cancel">Cancel</button>
            </div>
        </modal>
    </div>
</template>

<script>
import Vue from "vue";
import Awesomplete from "awesomplete";
import modal from "@vue-utils/bootstrap-modal.vue";
import datatable from "@vue-utils/datatable.vue";
import { mapGetters, mapActions } from "vuex";
import { api_endpoints, helpers, cache_helper } from "@/utils/hooks";
import MapLocationOffence from "./map_location_offence1";
import SearchPersonOrganisation from "@common-components/search_person_or_organisation.vue";
//import CreateNewPerson from "@common-components/create_new_person.vue";
import utils from "../utils";
import $ from "jquery";
//import "bootstrap/dist/css/bootstrap.css";
import "awesomplete/awesomplete.css";
import { v4 as uuidv4 } from 'uuid';
import "jquery-ui/ui/widgets/draggable.js";
import FileField from '@/components/common/compliance_file.vue';

export default {
  name: "Offence",
  data: function() {
    let vm = this;

    vm.max_items = 20;
    vm.ajax_for_alleged_offence = null;
    vm.ajax_for_offender = null;
    vm.suggest_list = []; // This stores a list of alleged offences displayed after search.
    vm.suggest_list_offender = []; // This stores a list of alleged offences displayed after search.
    vm.awe = null;

    return {
      uuid: 0,
      displayCreateNewPerson: false,
      updatingContact: false,
      newPersonBeingCreated: false,
      officers: [],
      isModalOpen: false,
      processingDetails: false,
      current_alleged_offence: {
        id: null,
        act: "",
        section_regulation: "",
        offence_text: ""
      },
      current_offender: null,
      offender_search_type: "individual",
      oTab: "oTab" + vm._uid,
      dTab: "dTab" + vm._uid,
      pTab: "pTab" + vm._uid,
      lTab: "lTab" + vm._uid,
      documentTab: 'documentTab' + vm._uid,
      errorResponse: '',

      temporary_document_collection_id: null,

      // regionDistricts: [],
      regions: [], // this is the list of options
      availableDistricts: [], // this is generated from the regionDistricts[] above

      dtHeadersOffender: ["id", "Individual/Organisation", "Details", "Action"],
      dtHeadersAllegedOffence: [
        "id",
        "Act",
        "Section/Regulation",
        "Alleged Offence",
        "Action"
      ],
      dtOptionsOffender: {
        columns: [
          {
            data: "id",
            visible: false
          },
          {
            data: "data_type",
            visible: true
          },
          {
            data: "data_type",
            render: function(data, type, row) {
              if (row.data_type == "individual") {
                let full_name = [row.first_name, row.last_name]
                  .filter(Boolean)
                  .join(" ");
                let email = row.email ? "E:" + row.email : "";
                let p_number = row.phone_number ? "P:" + row.phone_number : "";
                let m_number = row.mobile_number
                  ? "M:" + row.mobile_number
                  : "";
                let dob = row.dob ? "DOB:" + row.dob : "DOB: ---";
                let myLabel = [
                  "<strong>" + full_name + "</strong>",
                  email,
                  p_number,
                  m_number,
                  dob
                ]
                  .filter(Boolean)
                  .join("<br />");

                return myLabel;
              } else if (row.data_type == "organisation") {
                let name = row.name ? row.name : "";
                let abn = row.abn ? "ABN:" + row.abn : "";
                let myLabel = ["<strong>" + name + "</strong>", abn]
                  .filter(Boolean)
                  .join("<br />");

                return myLabel;
              }
            }
          },
          {
            data: "id",
            render: function(data, type, row) {
              return (
                '<a href="#" class="remove_button" data-offender-id="' +
                row.id +
                '">Remove</a>'
              );
            }
          }
        ]
      },
      dtOptionsAllegedOffence: {
        columns: [
      //    {
      //      data: "id",
      //      visible: false
      //    },
      //    {
      //      data: "Act"
      //    },
      //    {
      //      data: "Section/Regulation"
      //    },
      //    {
      //      data: "Alleged Offence"
      //    },
      //    {
      //      data: "Action",
      //      mRender: function(data, type, row) {
      //        return (
      //          '<a href="#" class="remove_button" data-alleged-offence-id="' +
      //          row.id +
      //          '">Remove</a>'
      //        );
      //      }
      //    }
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
                            return ret_str;
                        }
                    },
                    {
                        data: 'allegedOffence',
                        render: function(data, type, row) {
                            let ret_str = row.allegedOffence.section_regulation.name;
                            return ret_str;
                        }
                    },
                    {
                        data: 'allegedOffence',
                        render: function(data, type, row) {
                            let ret_str = row.allegedOffence.section_regulation.offence_text;
                            return ret_str;
                        }
                    },
                    {
                        data: 'allegedOffence',
                        render: function(data, type, row) {
                            let ret_str = '<a href="#" class="remove_button" data-alleged-offence-uuid="' + row.allegedOffence.uuid + '">Remove</a>';
                            return ret_str;
                        }
                    },
        ]
      }
    };

  },
  components: {
      modal,
      datatable,
      MapLocationOffence,
      SearchPersonOrganisation,
      FileField,
    //CreateNewPerson
  },
    props:{
      region_id: {
          required: false,
          default: null,
      },
      district_id: {
          required: false,
          default: null,
      },
      // allocated_group_id: {
      //     required: false,
      //     default: null,
      // },
  },
  computed: {
    ...mapGetters("offenceStore", {
      offence: "offence"
    }),
    ...mapGetters('inspectionStore', {
      inspection: "inspection",
    }),
    ...mapGetters('legalCaseStore', {
      legal_case: "legal_case",
    }),
    ...mapGetters('callemailStore', {
      call_email: "call_email",
    }),
    parent_legal_case: function() {
        if (this.legal_case && this.legal_case.id) {
            return true;
        }
    },
    parent_call_email: function() {
        if (this.call_email && this.call_email.id) {
            return true;
        }
    },
    parent_inspection: function() {
        if (this.inspection && this.inspection.id) {
            return true;
        }
    },

    modalTitle: function() {
      return "Identify Offence";
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
    updateSearchPersonOrganisationBindId: function() {
        this.uuid += 1
        return 'offender' + this.uuid
    },
    parentEntity: function() {
        return {'id': 1, 'data_type': 'individual'}
    },
  },
  filters: {
    formatDate: function(data) {
      return data ? moment(data).format("DD/MM/YYYY HH:mm:ss") : "";
    }
  },
  methods: {
    ...mapActions("offenceStore", {
      setAllegedOffenceIds: "setAllegedOffenceIds",
      setOffenders: "setOffenders",
      setCallEmailId: "setCallEmailId",
      setRegionId: "setRegionId",
      setDistrictId: "setDistrictId",
      // setAllocatedGroupId: "setAllocatedGroupId",
      setInspectionId: "setInspectionId",
      setLegalCaseId: "setLegalCaseId",
      createOffence: "createOffence",
      setOffenceEmpty: "setOffenceEmpty",
      setTempDocumentCollectionId: "setTempDocumentCollectionId",
    }),
    ...mapActions('inspectionStore', {
      loadInspection: "loadInspection",
    }),
    ...mapActions('callemailStore', {
      loadCallEmail: "loadCallEmail",
    }),
    ...mapActions('legalCaseStore', {
      loadLegalCase: "loadLegalCase",
    }),
        setTemporaryDocumentCollectionId: function(val) {
            this.temporary_document_collection_id = val;
        },
    makeModalsDraggable: function(){
        this.elem_modal = $('.modal > .modal-dialog');
        for (let i=0; i<this.elem_modal.length; i++){
            //$(this.elem_modal[i]).draggable();
        }
    },
    constructRegionsAndDistricts: async function() {
        let returned_regions = await cache_helper.getSetCacheList(
            "Regions",
            "/api/regions/"
        );
        Object.assign(this.regions, returned_regions);
        this.regions.splice(0, 0, {
            id: "",
            name: "",
            district: "",
            districts: [],
            region: null
        });
        // let returned_region_districts = await cache_helper.getSetCacheList(
        //     "RegionDistricts",
        //     api_endpoints.region_district
        // );
        // Object.assign(this.regionDistricts, returned_region_districts);
    },
    newPersonCreated: function(obj) {
      if(obj.person){
        this.setCurrentOffender('individual', obj.person.id);

        // Set fullname and DOB into the input box
        let full_name = [obj.person.first_name, obj.person.last_name].filter(Boolean).join(" ");
        let dob = obj.person.dob ? "DOB:" + obj.person.dob : "DOB: ---";
        let value = [full_name, dob].filter(Boolean).join(", ");
        this.$refs.person_search.setInput(value);
      } else if (obj.err) {
        //console.log(err);
      } else {
        // Should not reach here
      }
    },
    personSelected: function(para) {
        let vm = this;
        vm.setCurrentOffender(para.data_type, para.id);
    },
    removeOffenderClicked: function(e) {
      let vm = this;

      let offenderId = parseInt(e.target.getAttribute("data-offender-id"));
      vm.$refs.offender_table.vmDataTable.rows(function(idx, data, node) {
        if (data.id === offenderId) {
          vm.$refs.offender_table.vmDataTable
            .row(idx)
            .remove()
            .draw();
        }
      });
    },
    removeClicked: function(e) {
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
    //    let vm = this;

    //    let allegedOffenceId = parseInt(
    //      e.target.getAttribute("data-alleged-offence-id")
    //    );
    //    vm.$refs.alleged_offence_table.vmDataTable.rows(function(
    //      idx,
    //      data,
    //      node
    //    ) {
    //      if (data.id === allegedOffenceId) {
    //        vm.$refs.alleged_offence_table.vmDataTable
    //          .row(idx)
    //          .remove()
    //          .draw();
    //      }
    //    });
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
    addOffenderClicked: async function() {
      let vm = this;

      if (
        vm.current_offender &&
        vm.current_offender.id &&
        vm.current_offender.data_type
      ) {
        // save person before adding to offender list
        await this.$refs.search_offender.parentSave()
        let already_exists = false;

        let ids = vm.$refs.offender_table.vmDataTable.columns(0).data()[0];
        let data_types = vm.$refs.offender_table.vmDataTable
          .columns(1)
          .data()[0];

        for (let i = 0; i < ids.length; i++) {
          if (
            ids[i] == vm.current_offender.id &&
            data_types[i] == vm.current_offender.data_type
          ) {
            already_exists = true;
            break;
          }
        }

        if (!already_exists) {
          if (vm.current_offender.data_type == "individual") {
            vm.$refs.offender_table.vmDataTable.row
              .add({
                data_type: vm.current_offender.data_type,
                id: vm.current_offender.id,
                first_name: vm.current_offender.first_name,
                last_name: vm.current_offender.last_name,
                email: vm.current_offender.email,
                p_number: vm.current_offender.p_number,
                m_number: vm.current_offender.m_numberum,
                dob: vm.current_offender.dob
              })
              .draw();
          } else if (vm.current_offender.data_type == "organisation") {
            vm.$refs.offender_table.vmDataTable.row
              .add({
                data_type: vm.current_offender.data_type,
                id: vm.current_offender.id,
                name: vm.current_offender.name,
                abn: vm.current_offender.abn
              })
              .draw();
          }
        }
      }

      vm.setCurrentOffenderEmpty();
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
                    section_regulation: {},
                    number_linked_sanction_outcomes_total: 0,
                    number_linked_sanction_outcomes_active: 0,
                    uuid: uuidv4()
                };
                Object.assign(alleged_offence_obj.section_regulation, this.current_alleged_offence);
                this.offence.alleged_offences.push(alleged_offence_obj);
            }
        }
        this.setCurrentAllegedOffenceEmpty();
        this.constructAllegedOffencesTable();
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
        this.$refs.alleged_offence_table.vmDataTable.row.add({ "allegedOffence": allegedOffence, "offence": this.offence }).draw();
    },
    ok: async function() {
        try {
            this.processingDetails = true;
            let response = await this.sendData();

            if (response.ok) {
                // Refresh offence table on the dashboard page
                if (this.$parent.$refs.offence_table){
                    this.$parent.$refs.offence_table.vmDataTable.ajax.reload();
                }

                // For Related items table
                if (this.parent_call_email) {
                    await this.loadCallEmail({
                        call_email_id: this.call_email.id,
                    });
                } else if (this.parent_legal_case) {
                    await this.loadLegalCase({
                        legal_case_id: this.legal_case.id,
                    });
                } else if (this.parent_inspection) {
                    await this.loadInspection({
                        inspection_id: this.inspection.id,
                    });
                }
            }

            if (this.$parent.$refs.related_items_table) {
                this.$parent.constructRelatedItemsTable();
            }

            this.setOffenceEmpty();
            this.close();
        } catch(err) {
            this.processError(err);
        } finally {
            this.processingDetails = false;
        }
    },
    processError: async function(err) {
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
                        errorText += field_name + ': ';
                        for (let j=0; j<err.body[field_name].length; j++){
                            errorText += err.body[field_name][j] + '<br />';
                        }
                    }
                }
            }
        } else {
            errorText += err.message;
        }
        this.errorResponse = errorText;
        //await swal("Error", errorText, "error");
    },
    cancel: function() {
        // for call_email offenceBindId
        if (this.$parent.call_email) {
            this.$parent.updateUuid();
        }

        this.processingDetails = false;
        this.close();
    },
    close: function() {
        this.processingDetails = false;
        this.isModalOpen = false;
    //    this.setOffenceEmpty();  // Make offence default
        //this.constructAllegedOffencesTable();
        //this.errorResponse = '';
    },
    mapOffenceClicked: function() {
      this.$refs.mapOffenceComponent.mapTabClicked();
    },
    sendData: async function() {
        let vm = this;

        // If exists, set call_email_id and other attributes to the offence
        if (this.$parent.call_email && this.$parent.call_email.id) {
            vm.setCallEmailId(this.$parent.call_email.id);
        }

        // If exists, set inspection_id to the offence
        if (this.$parent.inspection && this.$parent.inspection.id) {
            vm.setInspectionId(this.$parent.inspection.id);
        }

        // If exists, set legal_case_id to the offence
        if (this.$parent.legal_case && this.$parent.legal_case.id) {
            vm.setLegalCaseId(this.$parent.legal_case.id);
        }

        if (this.temporary_document_collection_id){
            vm.setTempDocumentCollectionId(this.temporary_document_collection_id)
        }

        // Collect offenders data from the datatable, and set them to the vuex
        let offenders = vm.$refs.offender_table.vmDataTable.rows().data().toArray();
        vm.setOffenders(offenders);

        let res = await vm.createOffence();;
        return res
    },
    addEventListeners: function() {
      let vm = this;
      let el_fr_date = $(vm.$refs.occurrenceDateFromPicker);
      let el_fr_time = $(vm.$refs.occurrenceTimeFromPicker);
      let el_to_date = $(vm.$refs.occurrenceDateToPicker);
      let el_to_time = $(vm.$refs.occurrenceTimeToPicker);

      // "Date From" field
      el_fr_date.datetimepicker({ format: "DD/MM/YYYY", maxDate: "now", showClear: true });
      el_fr_date.on("dp.change", function(e) {
        if (el_fr_date.data("DateTimePicker").date()) {
          vm.offence.occurrence_date_from = e.date.format("DD/MM/YYYY");
            el_to_date.data('DateTimePicker').minDate(e.date);
        } else if (el_fr_date.data("date") === "") {
          vm.offence.occurrence_date_from = null;
        }
      });
      // "Time From" field
      el_fr_time.datetimepicker({ format: "LT", showClear: true });
      el_fr_time.on("dp.change", function(e) {
        if (el_fr_time.data("DateTimePicker").date()) {
          vm.offence.occurrence_time_from = e.date.format("LT");
        } else if (el_fr_time.data("date") === "") {
          vm.offence.occurrence_time_from = null;
        }
      });

      // "Date To" field
      el_to_date.datetimepicker({ format: "DD/MM/YYYY", maxDate: "now", showClear: true });
      el_to_date.on("dp.change", function(e) {
        if (el_to_date.data("DateTimePicker").date()) {
          vm.offence.occurrence_date_to = e.date.format("DD/MM/YYYY");
            el_fr_date.data('DateTimePicker').maxDate(e.date);
        } else if (el_to_date.data("date") === "") {
          vm.offence.occurrence_date_to = null;
        }
      });
      // "Time To" field
      el_to_time.datetimepicker({ format: "LT", showClear: true });
      el_to_time.on("dp.change", function(e) {
        if (el_to_time.data("DateTimePicker").date()) {
          vm.offence.occurrence_time_to = e.date.format("LT");
        } else if (el_to_time.data("date") === "") {
          vm.offence.occurrence_time_to = null;
        }
      });

      $("#alleged-offence-table").on(
        "click",
        ".remove_button",
        vm.removeClicked
      );
      $("#offender-table").on(
        "click",
        ".remove_button",
        vm.removeOffenderClicked
      );
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
    markMatchedText(original_text, input) {
      let ret_text = original_text.replace(new RegExp(input, "gi"), function(
        a,
        b
      ) {
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
             * 
             * Structure of the awesomplete list
             * <ul>
             *     <li>
             *         <div data-item-id="id_number">
             *             <strong>
             *                 <mark>
             * User can click either <li>/<div>/<strong>/<mark>.
             * Therefore to get the <div> element, which has an item id, you need a bit of calculation.
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
      let vm = this;

      vm.current_offender = null;

      $("#offender_input").val("");
        vm.$refs.search_offender.clearInput();
    },
    setCurrentAllegedOffenceEmpty: function() {
      let vm = this;

      vm.current_alleged_offence.id = null;
      vm.current_alleged_offence.act = "";
      vm.current_alleged_offence.name = "";
      vm.current_alleged_offence.offence_text = "";

      $("#alleged-offence").val("");
    },
    currentRegionIdChanged: function() {
      this.updateDistricts();
    },
    updateDistricts: function(updateFromUI) {
      if (updateFromUI) {
        // We don't want to clear the default district selection when initially loaded, which derived from the call_email
        this.offence.district_id = null;
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
  },
    created: async function() {

        let self = this;
        self.setOffenceEmpty();
        self.$nextTick(function() {
            self.initAwesompleteAllegedOffence();
        });
        await this.constructRegionsAndDistricts();
        this.setRegionId(this.region_id);
        this.setDistrictId(this.district_id);
        // this.setAllocatedGroupId(this.allocated_group_id);
    },
    mounted: function() {
        this.$nextTick(() => {
            this.addEventListeners();
            this.makeModalsDraggable();
        });
    }
};
</script>

<style lang="css" scoped>
.btn-file {
  position: relative;
  overflow: hidden;
}
.btn-file input[type="file"] {
  position: absolute;
  top: 0;
  right: 0;
  min-width: 100%;
  min-height: 100%;
  font-size: 100px;
  text-align: right;
  filter: alpha(opacity=0);
  opacity: 0;
  outline: none;
  background: white;
  cursor: inherit;
  display: block;
}
.top-buffer {
  margin-top: 5px;
}
.top-buffer-2x {
  margin-top: 10px;
}
#offence-details {
}
.radio-button-label {
  padding-left: 0;
}
.tab-content {
  background: white;
  padding: 10px;
  border: solid 1px lightgray;
}
#DataTable {
  padding: 10px 5px;
  border: 1px solid lightgray;
}
</style>
