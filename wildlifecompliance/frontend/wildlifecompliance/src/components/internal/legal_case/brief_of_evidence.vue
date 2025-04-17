<template lang="html">
        <!--div class="col-md-9"-->
            <div>
                <FormSection :formCollapse="false" label="Statement of Facts">
                    <div class="col-sm-12 form-group"><div class="row">
                        <label class="col-sm-10">Statement of facts
                            <textarea :readonly="readonlyForm" class="form-control location_address_field" v-model="briefOfEvidence.statement_of_facts" />
                        </label>
                    </div></div>
                </FormSection>
                <FormSection :formCollapse="false" label="Case Information Form">
                    <div class="col-sm-12 form-group"><div class="row">
                        <label class="col-sm-10">
                        <input :disabled="readonlyForm" type="checkbox" data-parsley-required v-model="briefOfEvidence.victim_impact_statement_taken" />
                        Victim impact statement to be taken?
                        </label>
                        <label v-if="briefOfEvidence.victim_impact_statement_taken" class="col-sm-10">Details
                            <textarea :readonly="readonlyForm" class="form-control location_address_field" v-model="briefOfEvidence.victim_impact_statement_taken_details" />
                        </label>
                        <label class="col-sm-10">
                        <!--input :onclick="readonlyBriefOfEvidence" type="checkbox" data-parsley-required v-model="briefOfEvidence.statements_pending" /-->
                        <input :disabled="readonlyForm" type="checkbox" data-parsley-required v-model="briefOfEvidence.statements_pending" />
                        Witness (including expert statements) still to be taken?
                        </label>
                        <label v-if="briefOfEvidence.statements_pending" class="col-sm-10">Details
                            <textarea :readonly="readonlyForm" class="form-control location_address_field" v-model="briefOfEvidence.statements_pending_details" />
                        </label>
                        <label class="col-sm-10">
                        <input :disabled="readonlyForm" type="checkbox" data-parsley-required v-model="briefOfEvidence.vulnerable_hostile_witnesses" />
                        Vulnerable / hostile witnesses?
                        </label>
                        <label v-if="briefOfEvidence.vulnerable_hostile_witnesses" class="col-sm-10">Details
                            <textarea :readonly="readonlyForm" class="form-control location_address_field" v-model="briefOfEvidence.vulnerable_hostile_witnesses_details" />
                        </label>
                        <label class="col-sm-10">
                        <input :disabled="readonlyForm" type="checkbox" data-parsley-required v-model="briefOfEvidence.witness_refusing_statement" />
                        Witnesses refusing to make statements?
                        </label>
                        <label v-if="briefOfEvidence.witness_refusing_statement" class="col-sm-10">Details
                            <textarea :readonly="readonlyForm" class="form-control location_address_field" v-model="briefOfEvidence.witness_refusing_statement_details" />
                        </label>
                        <label class="col-sm-10">
                        <input :disabled="readonlyForm" type="checkbox" data-parsley-required v-model="briefOfEvidence.problems_needs_prosecution_witnesses" />
                        Specific problems / needs of prosecution witnesses, e.g. interpreters?
                        </label>
                        <label v-if="briefOfEvidence.problems_needs_prosecution_witnesses" class="col-sm-10">Details
                            <textarea :readonly="readonlyForm" class="form-control location_address_field" v-model="briefOfEvidence.problems_needs_prosecution_witnesses" />
                        </label>
                        <label class="col-sm-10">
                        <input :disabled="readonlyForm" type="checkbox" data-parsley-required v-model="briefOfEvidence.accused_bad_character" />
                        History of bad character / propensity (similar fact) evidence involving accused?
                        </label>
                        <label v-if="briefOfEvidence.accused_bad_character" class="col-sm-10">Details
                            <textarea :readonly="readonlyForm" class="form-control location_address_field" v-model="briefOfEvidence.accused_bad_character_details" />
                        </label>
                        <label class="col-sm-10">
                        <input :disabled="readonlyForm" type="checkbox" data-parsley-required v-model="briefOfEvidence.further_persons_interviews_pending" />
                        Further persons (witness or suspect) to be interviewed?
                        </label>
                        <label v-if="briefOfEvidence.further_persons_interviews_pending" class="col-sm-10">Details
                            <textarea :readonly="readonlyForm" class="form-control location_address_field" v-model="briefOfEvidence.further_persons_interviews_pending_details" />
                        </label>
                        <label class="col-sm-10">
                        <input :disabled="readonlyForm" type="checkbox" data-parsley-required v-model="briefOfEvidence.other_interviews" />
                        Other persons whose details do not appear on this brief who have been interviewed?
                        </label>
                        <label v-if="briefOfEvidence.other_interviews" class="col-sm-10">Details
                            <textarea :readonly="readonlyForm" class="form-control location_address_field" v-model="briefOfEvidence.other_interviews_details" />
                        </label>
                        <label class="col-sm-10">
                        <input :disabled="readonlyForm" type="checkbox" data-parsley-required v-model="briefOfEvidence.relevant_persons_pending_charges" />
                        Other relevant persons charged or yet to be charged?
                        </label>
                        <label v-if="briefOfEvidence.relevant_persons_pending_charges" class="col-sm-10">Details
                            <textarea :readonly="readonlyForm" class="form-control location_address_field" v-model="briefOfEvidence.relevant_persons_pending_charges_details" />
                        </label>
                        <label class="col-sm-10">
                        <input :disabled="readonlyForm" type="checkbox" data-parsley-required v-model="briefOfEvidence.other_persons_receiving_sanction_outcome" />
                        Others receiving Infringement / Warning arising out of the same incident?
                        </label>
                        <label v-if="briefOfEvidence.other_persons_receiving_sanction_outcome" class="col-sm-10">Details
                            <textarea :readonly="readonlyForm" class="form-control location_address_field" v-model="briefOfEvidence.other_persons_receiving_sanction_outcome_details" />
                        </label>
                        <label class="col-sm-10">
                        <input :disabled="readonlyForm" type="checkbox" data-parsley-required v-model="briefOfEvidence.local_public_interest" />
                        Matters of local / public interest?
                        </label>
                        <label v-if="briefOfEvidence.local_public_interest" class="col-sm-10">Details
                            <textarea :readonly="readonlyForm" class="form-control location_address_field" v-model="briefOfEvidence.local_public_interest_details" />
                        </label>
                        <label class="col-sm-10">
                        <input :disabled="readonlyForm" type="checkbox" data-parsley-required v-model="briefOfEvidence.applications_orders_requests" />
                        Other applications / orders on conviction requests?
                        </label>
                        <label v-if="briefOfEvidence.applications_orders_requests" class="col-sm-10">Details
                            <textarea :readonly="readonlyForm" class="form-control location_address_field" v-model="briefOfEvidence.applications_orders_requests_details" />
                        </label>
                        <label class="col-sm-10">
                        <input :disabled="readonlyForm" type="checkbox" data-parsley-required v-model="briefOfEvidence.applications_orders_required" />
                        Are there any other applications / orders on conviction required?
                        </label>
                        <label v-if="briefOfEvidence.applications_orders_required" class="col-sm-10">Details
                            <textarea :readonly="readonlyForm" class="form-control location_address_field" v-model="briefOfEvidence.applications_orders_required_details" />
                        </label>
                        <label class="col-sm-10">
                        <input :disabled="readonlyForm" type="checkbox" data-parsley-required v-model="briefOfEvidence.other_legal_matters" />
                        Is there any statutory notice, DEC licence, ministerial statement or policy etc. re the matter, premise or person subject to this brief?
                        </label>
                        <label v-if="briefOfEvidence.other_legal_matters" class="col-sm-10">Details
                            <textarea :readonly="readonlyForm" class="form-control location_address_field" v-model="briefOfEvidence.other_legal_matters_details" />
                        </label>
                    </div></div>
                </FormSection>
                <FormSection :formCollapse="false" label="Offences, Offenders and Records of Interview" treeHeight="yes">
                    <div v-if="boeRoiExist">
                        <div v-if="boeRoiVisibility" class="col-sm-12 form-group"><div class="row">
                            <TreeSelect
                            id="boe-record-of-interview-tree"
                            ref="boe_record_of_interview_tree" 
                            :value="boeRoiTicked" 
                            :options="boeRoiOptions" 
                            :default-expand-level="Infinity" 
                            multiple
                            value-consists-of="LEAF_PRIORITY"
                            @input="setBoeRoiTicked"
                            alwaysOpen
                            :searchable="false"
                            />
                        </div></div>
                        <div v-else class="col-sm-12 form-group"><div class="row">
                            <div v-for="record in boeRoiOptions">
                                <span v-if="record.show">
                                    <a :href=record.hyperlink target="_blank">{{ record.label }}</a>
                                </span>
                                <span v-for="child in record.children">
                                    <span v-if="child.show">
                                        ; <a :href=child.hyperlink target="_blank">{{ child.label }}</a>
                                    </span>
                                    <span v-for="grandchild in child.children">
                                        <span v-if="grandchild.show">
                                            ; <a :href=grandchild.hyperlink target="_blank">{{ grandchild.label }}</a>
                                        </span>
                                        <span v-for="greatgrandchild in grandchild.children">
                                            <span v-if="greatgrandchild.show">
                                                ; <a :href=greatgrandchild.hyperlink target="_blank">{{ greatgrandchild.label }}</a>
                                            </span>
                                        </span>
                                    </span>
                                </span>
                            </div>
                        </div></div>
                    </div>
                    <span v-else class="col-sm-10">No Offences, Offenders or Records of Interview</span>
                </FormSection>
                <FormSection :formCollapse="false" label="Witness Statements, Officer Statements, Expert Statements" treeHeight="yes">
                    <div v-if="boeOtherStatementsExist">
                        <div v-if="boeOtherStatementsVisibility" class="col-sm-12 form-group"><div class="row">
                            <TreeSelect 
                            id="boe-other-statements-tree"
                            ref="boe_other_statements_tree" 
                            :value="boeOtherStatementsTicked" 
                            :options="boeOtherStatementsOptions" 
                            :default-expand-level="Infinity" 
                            multiple
                            value-consists-of="LEAF_PRIORITY"
                            @input="setBoeOtherStatementsTicked"
                            alwaysOpen
                            :searchable="false"
                            />
                        </div></div>
                        <div v-else class="col-sm-12 form-group"><div class="row">
                            <div v-for="record in boeOtherStatementsOptions">
                                <span v-if="record.show">
                                    <a :href=record.hyperlink target="_blank">{{ record.label }}</a>
                                </span>
                                <span v-for="child in record.children">
                                    <span v-if="child.show">
                                        ; <a :href=child.hyperlink target="_blank">{{ child.label }}</a>
                                    </span>
                                    <span v-for="grandchild in child.children">
                                        <span v-if="grandchild.show">
                                            ; <a :href=grandchild.hyperlink target="_blank">{{ grandchild.label }}</a>
                                        </span>
                                    </span>
                                </span>
                            </div>
                        </div></div>
                    </div>
                    <span v-else class="col-sm-10">No Witness Statements, Officer Statements or Expert Statements</span>
                </FormSection>
                <FormSection id="physical-artifacts-tree" :formCollapse="false" label="List of Exhibits, Sensitive Unused and Non-Sensitive Unused Materials" treeHeight="yes">
                    <div class="col-sm-12 form-group"><div class="row">
                        <label class="col-sm-10">Select the objects to be included on the list of exhibits</label>
                        <div class v-if="physicalArtifactsUsedVisibility" class="col-sm-10">
                            <div class="row" v-for="artifact in physicalArtifactsUsed">
                                <!--input class="col-sm-1" type="checkbox" :value="artifact.id" v-model="physicalArtifactsUsedTicked"-->
                                <input :disabled="readonlyForm" class="col-sm-1" type="checkbox" v-model="artifact.ticked">
                                <a :href=artifact.hyperlink target="_blank">{{ artifact.label }}</a>
                            </div>
                        </div>
                        <span v-else class="col-sm-10">No objects on the list of exhibits</span>
                        <label class="col-sm-10">Select the objects to be included on the sensitive unused list of materials</label>
                        <div v-if="physicalArtifactsSensitiveUnusedVisibility" class="col-sm-10">
                            <div class="row" v-for="artifact in physicalArtifactsSensitiveUnused">
                                <!--input class="col-sm-1" :id="'tickbox_' + artifact.id" type="checkbox" :value="artifact.id" v-model="physicalArtifactsSensitiveUnusedTicked"-->
                                <input :disabled="readonlyForm" class="col-sm-1" :id="'tickbox_' + artifact.id" type="checkbox" v-model="artifact.ticked">
                                <!--label class="col-sm-3">{{ artifact.label }}</label-->
                                <a :href=artifact.hyperlink target="_blank">{{ artifact.label }}</a>
                                <div v-if="artifact.ticked">
                                    <label class="col-sm-3">Reason for sensitivity / non-disclosure</label>
                                    <div class="col-sm-5">
                                        <textarea 
                                            class="form-control" 
                                            v-model="artifact.reason_sensitive_non_disclosable" 
                                            :id="'reason_' + artifact.physical_artifact_id"
                                            :readonly="readonlyForm" 
                                            />
                                    </div>
                                </div>
                            </div>
                        </div>
                        <span v-else class="col-sm-10">No objects on the sensitive unused list of materials</span>
                        <label class="col-sm-10">Select the objects to be included on the non-sensitive unused list of materials</label>
                        <div v-if="physicalArtifactsNonSensitiveUnusedVisibility" class="col-sm-10">
                            <div class="row" v-for="artifact in physicalArtifactsNonSensitiveUnused">
                                <!--input class="col-sm-1" type="checkbox" :value="artifact.id" v-model="physicalArtifactsNonSensitiveUnusedTicked"-->
                                <input :disabled="readonlyForm" class="col-sm-1" type="checkbox" v-model="artifact.ticked">
                                <!--label class="col-sm-4">{{ artifact.label }}</label-->
                                <a :href=artifact.hyperlink target="_blank">{{ artifact.label }}</a>
                            </div>
                        </div>
                        <span v-else class="col-sm-10">No objects on the non-sensitive unused list of materials</span>
                    </div></div>
                </FormSection>
                <FormSection :formCollapse="false" label="List of Photographic, Video and Sound Exhibits">
                    <div v-if="documentArtifactsVisibility" class="col-sm-12 form-group"><div class="row">
                        <div class="row" v-for="artifact in documentArtifacts">
                            <!--input class="col-sm-1" type="checkbox" :value="artifact.id" v-model="physicalArtifactsUsedTicked"-->
                            <input :disabled="readonlyForm" class="col-sm-1" type="checkbox" v-model="artifact.ticked">
                            <a :href=artifact.hyperlink target="_blank">{{ artifact.label }}</a>
                            <!--label class="col-sm-4">
                                {{ artifact.label }}
                            </label-->
                            <div class="col-sm-12 form-group document-artifact-file"><div class="row">
                                <div v-for="document in artifact.attachments">
                                    <label> {{ document.name }}
                                        <div v-if="['png', 'jpg'].includes(document.type)">
                                            <img class="col-sm-4" :src="document.file" alt="image file"/>
                                        </div>
                                        <div v-else-if="['mp4'].includes(document.type)">
                                            <video width="82" height="82" controls>
                                                <source :src="document.file" type="video/mp4">
                                            </video>
                                        </div>
                                    </label>
                                </div>
                            </div></div>
                        </div>
                    </div></div>
                    <span v-else class="col-sm-10">No Photographic, Video or Sound Exhibits</span>
                </FormSection>
                <FormSection :formCollapse="false" label="Additional Documents">
                    <div class="col-sm-12 form-group"><div class="row">
                        <filefield 
                        ref="brief_of_evidence_documents" 
                        name="brief-of-evidence-documents" 
                        :isRepeatable="true" 
                        :documentActionUrl="legal_case.briefOfEvidenceDocumentUrl" 
                        :readonly="readonlyForm"
                        v-bind:key="legal_case.briefOfEvidenceDocumentUrl"
                        />
                    </div></div>
                </FormSection>
            </div>
        <!--/div-->
</template>
<script>
import Vue from "vue";
import FormSection from "@/components/forms/section_toggle.vue";
import { api_endpoints, helpers, cache_helper } from "@/utils/hooks";
import utils from "@/components/external/utils";
import { mapState, mapGetters, mapActions, mapMutations } from "vuex";
import moment from 'moment';
//import 'bootstrap/dist/css/bootstrap.css';
//import 'eonasdan-bootstrap-datetimepicker';
require("select2/dist/css/select2.min.css");
require("select2-bootstrap-theme/dist/select2-bootstrap.min.css");
import _ from 'lodash';
import TreeSelect from '@riophae/vue-treeselect'
import '@riophae/vue-treeselect/dist/vue-treeselect.css'
import filefield from '@/components/common/compliance_file.vue';


export default {
    name: "ViewBriefOfEvidence",
    data: function() {
        return {
            uuid: 0,
      };
  },
  components: {
    FormSection,
    TreeSelect,
    filefield,
  },
  props:{
        readonly: {
            type: Boolean,
            default: true,
        },
  },
    /*
  watch: {
      readonlyForm: {
          handler: function (newVal, oldVal){
              this.showHideTreeControls();
          },
          deep: true
      },
  },
  */
  computed: {
    ...mapGetters('legalCaseStore', {
      legal_case: "legal_case",
    }),
    csrf_token: function() {
      return helpers.getCookie("csrftoken");
    },
    briefOfEvidence: function() {
        if (this.legal_case && this.legal_case.brief_of_evidence) {
            return this.legal_case.brief_of_evidence;
        } else {
            return {}
        }
    },
    physicalArtifactsUsed: function() {
        let options = [];
        if (this.legal_case && this.legal_case.boe_physical_artifacts_used) {
            for (let option of this.legal_case.boe_physical_artifacts_used) {
                options.push(option);
            }
        }
        return options;
    },
    physicalArtifactsUsedVisibility: function() {
        let visible = false;
        if (this.physicalArtifactsUsed && this.physicalArtifactsUsed.length > 0) {
            visible = true;
        }
        return visible
    },
    physicalArtifactsSensitiveUnused: function() {
        let options = [];
        if (this.legal_case && this.legal_case.boe_physical_artifacts_sensitive_unused) {
            for (let option of this.legal_case.boe_physical_artifacts_sensitive_unused) {
                options.push(option);
            }
        }
        return options;
    },
    physicalArtifactsSensitiveUnusedVisibility: function() {
        let visible = false;
        if (this.physicalArtifactsSensitiveUnused && this.physicalArtifactsSensitiveUnused.length > 0) {
            visible = true;
        }
        return visible
    },
    physicalArtifactsNonSensitiveUnused: function() {
        let options = [];
        if (this.legal_case && this.legal_case.boe_physical_artifacts_non_sensitive_unused) {
            for (let option of this.legal_case.boe_physical_artifacts_non_sensitive_unused) {
                options.push(option);
            }
        }
        return options;
    },
    physicalArtifactsNonSensitiveUnusedVisibility: function() {
        let visible = false;
        if (this.physicalArtifactsNonSensitiveUnused && this.physicalArtifactsNonSensitiveUnused.length > 0) {
            visible = true;
        }
        return visible
    },
    documentArtifactsVisibility: function() {
        let visible = false;
        if (this.documentArtifacts && this.documentArtifacts.length > 0) {
            visible = true;
        }
        return visible;
    },
    readonlyForm: function() {
        let readonly = true
        if (this.legal_case && this.legal_case.id && !this.readonly) {
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
    boeRoiTicked: function() {
        let ticked = []
        if (this.legal_case && this.legal_case.boe_roi_ticked) {
            for (let id of this.legal_case.boe_roi_ticked) {
                ticked.push(id)
            }
        }
        return ticked;
    },
    boeOtherStatementsTicked: function() {
        let ticked = []
        if (this.legal_case && this.legal_case.boe_other_statements_ticked) {
            for (let id of this.legal_case.boe_other_statements_ticked) {
                ticked.push(id)
            }
        }
        return ticked;
    },
    boeOtherStatementsOptions: function() {
        let options = [];
        if (this.legal_case && this.legal_case.boe_other_statements_options) {
            options = this.legal_case.boe_other_statements_options;
        }
        return options;
    },
    boeOtherStatementsExist: function() {
        let visibility = false;
        if (this.boeOtherStatementsOptions && this.boeOtherStatementsOptions.length > 0) {
            visibility = true;
        }
        return visibility;
    },
    boeOtherStatementsVisibility: function() {
        let visibility = false;
        if (!this.readonlyForm && this.boeOtherStatementsExist) {
            visibility = true;
        }
        return visibility;
    },
    boeRoiOptions: function() {
        let options = [];
        if (this.legal_case && this.legal_case.boe_roi_options) {
            options = this.legal_case.boe_roi_options;
        }
        return options;
    },
    boeRoiExist: function() {
        let visibility = false;
        if (this.boeRoiOptions && this.boeRoiOptions.length > 0) {
            visibility = true;
        }
        return visibility;
    },
    boeRoiVisibility: function() {
        let visibility = false;
        if (!this.readonlyForm && this.boeRoiExist) {
        //if (this.boeRoiOptions && this.boeRoiOptions.length > 0) {
            visibility = true;
        }
        return visibility;
    },
    documentArtifacts: function() {
        let options = [];
        if (this.legal_case && this.legal_case.boe_document_artifacts) {
            for (let option of this.legal_case.boe_document_artifacts) {
                options.push(option);
            }
        }
        return options;
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
      saveLegalCase: 'saveLegalCase',
      setLegalCase: 'setLegalCase',
      setBoeRoiTicked: 'setBoeRoiTicked',
      setBoeOtherStatementsTicked: 'setBoeOtherStatementsTicked',
      setBoePhysicalArtifactsTicked: 'setBoePhysicalArtifactsTicked',
      setBoeDocumentArtifactsTicked: 'setBoeDocumentArtifactsTicked',
    }),
      /*
    showHideTreeControls: function() {
        //let vm = this;
        //console.log(this.readonlyForm);
        if (this.readonlyForm) {
            this.$nextTick(() => {
                //console.log("true");
                $("#boe-record-of-interview-tree").find(".vue-treeselect__control").css("display", "block");
                $("#boe-other-statements-tree").find(".vue-treeselect__control").css("display", "block");
            });
        } else {
            this.$nextTick(() => {
                //console.log("false");
                $('#boe-record-of-interview-tree').find(".vue-treeselect__control").css("display", "none");
                $("#boe-other-statements-tree").find(".vue-treeselect__control").css("display", "none");
            });
        }
    },
    */
  },
  created: async function() {
  },
  mounted: function() {
      this.$nextTick(() => {
          $('.vue-treeselect__control').css("display", "none");
          //this.showHideTreeControls();
          /*
          if (this.$refs.boe_record_of_interview_tree) {
              $('#boe-record-of-interview-tree').find(".vue-treeselect__control").css("display", "none");
          }
          if (this.$refs.boe_other_statements_tree) {
              $("#boe-other-statements-tree").find(".vue-treeselect__control").css("display", "none");
          }
          */
        });
  },
};
</script>

<style lang="css">
.action-button {
    margin-top: 5px;
}
.document-artifact-file {
    margin-left: 70px;
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
