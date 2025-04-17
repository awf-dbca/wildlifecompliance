<template lang="html">
    <div class="container">
      <div class="row">
        <div class="col-md-3">
          <h3>Call/Email: {{ call_email.number }}</h3>
        </div>
        <div class="col-md-3 pull-right">
          <input  v-if="call_email.user_is_volunteer" type="button" @click.prevent="duplicate" class="pull-right btn btn-primary" value="Create Duplicate Call/Email"/>  
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

                        <!--div v-if="call_email.allocated_group && !(statusId === 'closed')" class="form-group"-->
                        <div v-if="assignToVisible" class="form-group">
                          <div class="row">
                            <div class="col-sm-12 top-buffer-s">
                              <strong>Currently assigned to</strong><br/>
                            </div>
                          </div>
                          <div class="row">
                            <div class="col-sm-12">
                              <select :disabled="!call_email.user_in_group" class="form-control" v-model="call_email.assigned_to_id" @change="updateAssignedToId()">
                                <option  v-for="option in call_email.allocated_group" :value="option.id" v-bind:key="option.id">
                                  {{ option.full_name }} 
                                </option>
                              </select>
                            </div>
                          </div>
                          <div v-if="call_email.user_in_group">
                              <a @click="updateAssignedToId('current_user')" class="btn pull-right">
                                  Assign to me
                              </a>
                          </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        Action 
                    </div>
                    <div class="panel-body panel-collapse">
                        <div v-if="statusId ==='draft' && canUserAction" class="row action-button">
                          <div class="col-sm-12">
                                <a ref="forwardToWildlifeProtectionBranch" @click="addWorkflow('forward_to_wildlife_protection_branch')" class="btn btn-primary btn-block">
                                  Forward to Wildlife Protection Branch
                                </a>
                          </div>
                        </div>
                        <!-- <div class="row">
                          <div class="col-sm-12"/>
                        </div> -->
                        <div v-if="statusId ==='draft' && canUserAction" class="row action-button">
                          <div class="col-sm-12">
                                <a ref="forwardToRegions" @click="addWorkflow('forward_to_regions')" class="btn btn-primary btn-block">
                                  Forward to Regions
                                </a>
                          </div>
                        </div>

                        <!--div v-if="statusId ==='open' && canUserAction" class="row action-button">
                          <div class="col-sm-12">
                                <a ref="save" @click="save()" class="btn btn-primary btn-block">
                                  Save
                                </a>
                          </div>
                        </div-->

                        <!-- <div class="row">
                          <div class="col-sm-12"/>
                        </div> -->
                        <div v-if="statusId ==='open_followup' && canUserAction" class="row action-button">

                        <!-- <div v-if="statusId ==='open_followup'" class="row action-button"> -->
                        <!-- <div class="row action-button"> -->

                          <div class="col-sm-12">
                                <a @click="openOffence()" class="btn btn-primary btn-block">
                                  Offence
                                </a>
                          </div>
                        </div>

                        <div v-if="statusId ==='open_followup' && canUserAction && this.offenceExists" class="row action-button">
                          <div class="col-sm-12">
                                <a @click="openSanctionOutcome()" class="btn btn-primary btn-block">
                                  Sanction Outcome
                                </a>
                          </div>
                        </div>
                        <!-- Following 3 actions are temporarily commented out  -->
                        <div v-if="statusId ==='open' && canUserAction" class="row action-button">
                          <div class="col-sm-12">
                                <a ref="allocateForFollowUp" @click="addWorkflow('allocate_for_follow_up')" class="btn btn-primary btn-block" >
                                  Allocate for Follow Up
                                </a>
                          </div>
                        </div>
                        <div v-if="statusId ==='open' && canUserAction" class="row action-button">
                          <div class="col-sm-12">
                                <a ref="allocateForInspection" @click="allocateForInspection()" class="btn btn-primary btn-block" >
                                  Allocate for Inspection
                                </a>
                          </div>
                        </div>
                        <div v-if="statusId ==='open' && canUserAction" class="row action-button">
                          <div class="col-sm-12">
                                <a ref="allocateForLegalCase" @click="allocateForLegalCase()" class="btn btn-primary btn-block" >
                                  Allocate for Case
                                </a>
                          </div>
                        </div>
                        <div v-if="closeButtonVisibility && canUserAction" class="row action-button">
                          <div class="col-sm-12">
                                <a ref="close" @click="addWorkflow('close')" class="btn btn-primary btn-block">
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
                        <li class="nav-item active"><a data-toggle="tab" :href="'#'+cTab">Call/Email</a></li>
                        <li class="nav-item"><a data-toggle="tab" :href="'#'+rTab">Related Items</a></li>
                    </ul>
                    <div class="tab-content">
                        <div :id="cTab" class="tab-pane fade in active">

                          <FormSection :formCollapse="false" label="Caller" Index="0">
                            
                            <div class="row"><div class="col-sm-8 form-group">
                              <label class="col-sm-12">Caller name</label>
                              <input :readonly="readonlyForm" class="form-control" v-model="call_email.caller"/>
                            </div></div>
                            <div class="col-sm-4 form-group"><div class="row">
                              <label class="col-sm-12">Caller contact information</label>
                            <input :readonly="readonlyForm" class="form-control" v-model="call_email.caller_phone_number"/>
                            </div></div>
                            
                            <div class="col-sm-12 form-group"><div class="row">
                              <label class="col-sm-4">Anonymous call?</label>
                                <input :disabled="readonlyForm" class="col-sm-1" id="anon_yes" type="radio" v-model="call_email.anonymous_call" v-bind:value="true">
                                <label class="col-sm-1" for="anon_yes">Yes</label>
                                <input :disabled="readonlyForm" class="col-sm-1" id="anon_no" type="radio" v-model="call_email.anonymous_call" v-bind:value="false">
                                <label class="col-sm-1" for="anon_no">No</label>
                            </div></div>
            
                            <!--div class="col-sm-12 form-group"><div class="row">
                              <label class="col-sm-4">Caller wishes to remain anonymous?</label>
                                <input :disabled="readonlyForm" class="col-sm-1" id="call_anon_yes" type="radio" v-model="call_email.caller_wishes_to_remain_anonymous" v-bind:value="true">
                                <label class="col-sm-1" for="call_anon_yes">Yes</label>
                                <input :disabled="readonlyForm" class="col-sm-1" id="call_anon_no" type="radio" v-model="call_email.caller_wishes_to_remain_anonymous" v-bind:value="false">
                                <label class="col-sm-1" for="call_anon_no">No</label>
                            </div></div-->
            
                            <div v-show="statusId !=='draft'">
                                <SearchPersonOrganisation 
                                :parentEntity="callerEntity"
                                :isEditable="personSearchVisibility" 
                                classNames="form-control" 
                                initialSearchType="individual" 
                                @entity-selected="entitySelected" 
                                showCreateUpdate
                                personOnly
                                ref="search_person_organisation"
                                v-bind:key="updateSearchPersonOrganisationBindId"/>
                            </div>
                          </FormSection>
            
                          <FormSection :formCollapse="false" label="Location *" Index="1">
                              <div v-if="call_email.location">
                                <MapLocation 
                                :isReadonly="readonlyForm"
                                v-bind:key="call_email.location.id"/>
                              </div>
                          </FormSection>
            
                          <FormSection :formCollapse="false" label="Details" Index="2">
                            <div class="col-sm-12 form-group"><div class="row">
                                <label class="col-sm-3">Date of call</label>
                                <div class="col-sm-3">
                                    <div class="input-group date" ref="dateOfCallPicker">
                                        <input :disabled="readonlyForm" type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="call_email.date_of_call"/>
                                        <span class="input-group-addon">
                                            <span class="glyphicon glyphicon-calendar"></span>
                                        </span>
                                    </div>
                                </div>
                                <label class="col-sm-3">Time of call</label>
                                <div class="col-sm-3">
                                    <div class="input-group date" id="timeOfCallPicker">
                                      <input :disabled="readonlyForm" type="text" class="form-control" placeholder="HH:MM" v-model="call_email.time_of_call"/>
                                      <span class="input-group-addon">
                                          <span class="glyphicon glyphicon-calendar"></span>
                                      </span>
                                    </div>
                                </div>
                            </div></div>
                            <div class="col-sm-12 form-group"><div class="row">
                              <label class="col-sm-3">Volunteer</label>
                            <div class="col-sm-9">
                              <select :disabled="readonlyForm" class="form-control" v-model="call_email.volunteer_id">
                                <option  v-for="option in call_email.volunteer_list" :value="option.id" v-bind:key="option.id">
                                  {{ option.full_name }} 
                                </option>
                              </select>
                            </div>
                            </div></div>
            
                            <div class="col-sm-12 form-group"><div class="row">
                              <label class="col-sm-3">Use occurrence from/to</label>
                              <div class="col-sm-2">
                                <input :disabled="readonlyForm" type="radio" id="occurenceYes" v-model="call_email.occurrence_from_to" v-bind:value="true">
                                <label for="occurenceYes">Yes</label>
                              </div>
                              <div class="col-sm-2">
                                <input :disabled="readonlyForm" type="radio" id="occurenceNo" v-model="call_email.occurrence_from_to" v-bind:value="false">
                                <label for="occurenceNo">No</label>
                              </div>
                            </div></div>
            
                            <div class="col-sm-12 form-group"><div class="row">
                                <label class="col-sm-3">{{ occurrenceDateLabel }}</label>
                                <div class="col-sm-4">
                                    <div class="input-group date" ref="occurrenceDateFromPicker">
                                        <input :disabled="readonlyForm" type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="call_email.occurrence_date_from" />
                                        <span class="input-group-addon">
                                            <span class="glyphicon glyphicon-calendar"></span>
                                        </span>
                                    </div>
                                </div>
                                <div v-show="call_email.occurrence_from_to">
                                    <div class="col-sm-4">
                                        <div class="input-group date" ref="occurrenceDateToPicker">
                                            <input :disabled="readonlyForm" type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="call_email.occurrence_date_to" />
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
                                  <div class="input-group date" id="occurrenceTimeStartPicker">
                                    <input :disabled="readonlyForm" type="text" class="form-control" placeholder="HH:MM" v-model="call_email.occurrence_time_start"/>
                                    <span class="input-group-addon">
                                        <span class="glyphicon glyphicon-calendar"></span>
                                    </span>
                                  </div>
                              </div>
                              <div v-show="call_email.occurrence_from_to">
                                  <label class="col-sm-3">Occurrence time to</label>
                                  <div class="col-sm-3">
                                      <div class="input-group date" id="occurrenceTimeEndPicker">
                                        <input :disabled="readonlyForm" type="text" class="form-control" placeholder="HH:MM" v-model="call_email.occurrence_time_end"/>
                                        <span class="input-group-addon">
                                            <span class="glyphicon glyphicon-calendar"></span>
                                        </span>
                                      </div>
                                  </div>
                              </div>
                            </div></div>
              
                            <div class="col-sm-12 form-group"><div class="row">
                              <label class="col-sm-3">Classification *</label>
                              <!-- <select :disabled="readonlyForm" class="form-control" v-model="call_email.classification_id">
                                    <option v-for="option in classification_types" :value="option.id" v-bind:key="option.id">
                                      {{ option.display }} 
                                    </option>
                                </select> -->
                              <div>
                                <div v-for="option in classification_types" class="col-sm-3">
                                  <input :disabled="readonlyForm" type="radio" v-bind:value="option.id" v-bind:key="option.id" :id="'classification_'+option.id" v-model="call_email.classification_id">
                                  <label :for="'classification_'+option.id">{{ option.display }}</label>
                                </div>
                              </div>
                            </div></div>

                             <div class="col-sm-12 form-group"><div class="row">
                              <label class="col-sm-3">Call Type *</label>
                              <div  class="col-sm-9">
                                <div v-for="option in call_types">
                                  <input :disabled="readonlyForm"  @change="filterWildcareSpeciesType($event,option.all_wildcare_species)" type="radio" v-bind:value="option.id" :id="'call_type_'+option.id" v-model="call_email.call_type_id">
                                   <label :for="'call_type_'+option.id">{{ option.display }}</label>
                                </div>
                              </div>
                            </div></div>

                            <div class="col-sm-12 form-group"><div class="row">
                              <label class="col-sm-3">Wildcare Species Type</label>
                              <div class="col-sm-9">
                              <select :disabled="readonlyForm" class="form-control" @change="filterWildcareSpeciesSubType()" v-model="call_email.wildcare_species_type_id">
                                    <option v-for="option in filter_wildcare_species_types" :value="option.id" v-bind:key="option.id" >
                                      {{ option.display }}
                                    </option>
                              </select>
                              </div>
                            </div></div>

                            <div class="col-sm-12 form-group"><div class="row">
                              <label class="col-sm-3">Wildcare Species Sub Type</label>
                              <div class="col-sm-9">
                              <select :disabled="speciesSubTypeDisabled" class="form-control" v-model="call_email.wildcare_species_sub_type_id">
                                    <option v-for="option in filter_wildcare_species_sub_types" :value="option.id" v-bind:key="option.id" >
                                      {{ option.display }}
                                    </option>
                              </select>
                              </div>
                            </div></div>

                            <!--div class="col-sm-12 form-group" v-if="speciesSubTypeDisabled">
                              <div class="row">
                                  <label class="col-sm-3">Species Name</label>
                                  <div class="col-sm-9">
                                    <input :disabled="readonlyForm" class="form-control" v-model="call_email.species_name"/>
                                  </div>
                              </div>
                            </div-->

                            <div class="col-sm-12 form-group"><div class="row">
                              <label class="col-sm-3">Age</label>
                              <div>
                                <div v-for="option in age_choices" class="col-sm-2">
                                  <input :disabled="readonlyForm" type="checkbox" :value="option.id" v-bind:key="option.id" :id="'age_'+option.id" v-model="call_email.age"/>
                                   <label :for="'age_'+option.id" >{{ option.display }}</label>
                                </div>
                              </div>
                            </div></div>

                            <div class="col-sm-12 form-group"><div class="row">
                              <label class="col-sm-3">Dead</label>
                              <div class="col-sm-2">
                                <input :disabled="readonlyForm" id="deadYes" type="radio" v-model="call_email.dead" value="true">
                                <label for="deadYes">Yes</label>
                              </div>
                              <div class="col-sm-2">
                                <input :disabled="readonlyForm" id="deadNo" type="radio" v-model="call_email.dead" value="false">
                                <label for="deadNo">No</label>
                              </div>
                            </div></div>

                            <div class="col-sm-12 form-group"><div class="row">
                              <label class="col-sm-3">Euthanise</label>
                              <div class="col-sm-2">
                                <input :disabled="readonlyForm" id="euthaniseYes" type="radio" v-model="call_email.euthanise" value="true">
                                <label for="euthaniseYes">Yes</label>
                              </div>
                              <div class="col-sm-2">
                                <input :disabled="readonlyForm" id="euthaniseNo" type="radio" v-model="call_email.euthanise" value="false">
                                <label for="euthaniseNo">No</label>
                              </div>
                            </div></div>

                             <div class="col-sm-12 form-group"><div class="row">
                              <label class="col-sm-3">Female / Male</label>
                              <div>
                                <div v-for="option in gender_choices" class="col-sm-2">
                                  <input :disabled="readonlyForm" type="checkbox" @change="checkFemalePinkyJoey" :value="option.id" :id="'gender_'+option.id" v-bind:key="option.id" v-model="call_email.gender"/>
                                   <label :for="'gender_'+option.id" >{{ option.display }}</label>
                                </div>
                              </div>
                            </div></div>

                            <div v-if="isFemalePinkyJoey" class="col-sm-12 form-group"><div class="row">
                              <label class="col-sm-3">Pinky / Joey</label>
                              <div>
                                <div v-for="option in baby_kangaroo_choices" class="col-sm-2">
                                  <input :disabled="readonlyForm" type="checkbox" :value="option.id" :id="'babyKangaroo'+option.id" v-bind:key="option.id" v-model="call_email.baby_kangaroo"/>
                                   <label :for="'babyKangaroo'+option.id">{{ option.display }}</label>
                                </div>
                              </div>
                            </div></div>

                            <div class="col-sm-12 form-group">
                              <div class="row">
                                  <label class="col-sm-3">Number of Animals</label>
                                  <div class="col-sm-9">
                                    <input :disabled="readonlyForm" class="form-control" v-model="call_email.number_of_animals" />
                                  </div>
                              </div>
                            </div>

                            <div class="col-sm-12 form-group">
                              <div class="row">
                                  <label class="col-sm-3">Brief nature of call *</label>
                                  <div class="col-sm-9">
                                    <textarea :disabled="readonlyForm" class="form-control" v-model="call_email.brief_nature_of_call" />
                                  </div>
                              </div>
                            </div>

                            <div class="col-sm-12 form-group"><div class="row">
                              <label class="col-sm-3">Entangled</label>
                              <div  class="col-sm-8" style="padding:0px">
                                <div v-for="option in entangled_choices" class="col-sm-4">
                                  <input :disabled="readonlyForm" type="checkbox" :value="option.id" v-bind:key="option.id" :id="'entangled_'+option.id" v-model="call_email.entangled"/>
                                   <label :for="'entangled_'+option.id" >{{ option.display }}</label>
                                </div>
                              </div>
                            </div></div>

                             <div v-if="isEntangledOther" class="col-sm-12 form-group">
                              <div class="row">
                                  <label class="col-sm-3">Entangled Other</label>
                                  <div class="col-sm-9">
                                    <input :disabled="readonlyForm" class="form-control" v-model="call_email.entangled_other"/>
                                  </div>
                              </div>
                            </div>

                           <!-- <div class="row">
                                <div class="col-sm-9 form-group">
                                  <label class="col-sm-4">Report Type</label>
                                  <select :disabled="readonlyForm" @change.prevent="loadSchema" class="form-control" v-model="call_email.report_type_id">
                                          <option v-for="option in report_types" :value="option.id" v-bind:key="option.id">
                                            {{ option.report_type }} 
                                          </option>
                                  </select>
                                </div>
                                <div class="col-sm-3 form-group">
                                    <div class="row">
                                        <label class="col-sm-2 advice-url-label">None </label>
                                    </div>
                                    <div class="row">
                                        <a v-if="reportAdviceUrl" class="advice-url" :href="reportAdviceUrl" target="_blank" >Advice</a>
                                    </div>
                                </div>
                            </div> -->
                            
                            <div v-if="rendererVisibility"  v-for="(item, index) in current_schema">
                              <compliance-renderer-block
                                 :component="item"
                                 :readonlyForm="readonlyForm"
                                 v-bind:key="`compliance_renderer_block_${index}`"
                                />
                            </div>
                          </FormSection>
            
                          <FormSection v-if="(call_email.referrer && call_email.referrer.length > 0) || call_email.advice_details" :formCollapse="true" label="Outcome" Index="3">
                            <div v-if="call_email.referrer && call_email.referrer.length > 0" class="col-sm-12 form-group"><div class="row">
                                <label class="col-sm-4">Referred To</label>
                                <select style="width:100%" disabled class="form-control input-sm" multiple="multiple" ref="referrerList" >
                                  <option  v-for="option in call_email.referrer" :value="option.id" v-bind:key="option.id">
                                    {{ option.name }} 
                                  </option>
                                </select>
                            </div></div>
                            <div v-if="call_email.advice_details" class="col-sm-12 form-group"><div class="row">
                              <label class="col-sm-4">Advice details</label>
                              <textarea :readonly="true" class="form-control" rows="5" v-model="call_email.advice_details"/>
                            </div></div>
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

        <div v-if="call_email.can_user_action" class="navbar navbar-fixed-bottom" style="background-color: #f5f5f5 ">
                        <div class="navbar-inner">
                            <div class="container">
                                <p class="pull-right" style="margin-top:5px;">
                                    
                                    <input type="button" @click.prevent="save('exit')" class="btn btn-primary" value="Save and Exit"/>
                                    <input type="button" @click.prevent="save('noexit')" class="btn btn-primary" value="Save and Continue" />
                                </p>
                            </div>
                        </div>
        </div>          
        <div v-if="workflow_type">
          <CallWorkflow ref="add_workflow" :workflow_type="workflow_type" v-bind:key="workflowBindId" />
        </div>
        <Offence 
        ref="offence" 
        :region_id="call_email.region_id" 
        :district_id="call_email.district_id" 
        :allocated_group_id="call_email.allocated_group_id" 
        v-bind:key="offenceBindId"/>
        <div v-if="sanctionOutcomeInitialised">
            <SanctionOutcome 
            ref="sanction_outcome" 
            />
        </div>
        <div v-if="inspectionInitialised">
            <Inspection 
             ref="inspection"
            />
        </div>
        <div v-if="legalCaseInitialised">
            <CreateLegalCaseModal 
            ref="legal_case"
            />
        </div>
    </div>
</template>
<script>
import Vue from "vue";
import FormSection from "@/components/forms/section_toggle.vue";

import CommsLogs from "@common-components/comms_logs.vue";
import MapLocation from "./map_location.vue";
import datatable from '@vue-utils/datatable.vue'
import { api_endpoints, helpers, cache_helper } from "@/utils/hooks";
//import SearchPerson from "./search_person.vue";
import SearchPersonOrganisation from "@common-components/search_person_or_organisation.vue";
import utils from "@/components/external/utils";
import { mapState, mapGetters, mapActions, mapMutations } from "vuex";
import moment from 'moment';
import CallWorkflow from './call_email_workflow';
import Offence from '../offence/offence_modal';
import SanctionOutcome from '../sanction_outcome/sanction_outcome_modal';
//import 'bootstrap/dist/css/bootstrap.css';
//import 'eonasdan-bootstrap-datetimepicker';
require("select2/dist/css/select2.min.css");
require("select2-bootstrap-theme/dist/select2-bootstrap.min.css");
import Inspection from '../inspection/create_inspection_modal';
import RelatedItems from "@common-components/related_items.vue";
import hash from 'object-hash';
import CreateLegalCaseModal from "../legal_case/create_legal_case_modal.vue";

export default {
  name: "ViewCallEmail",
  data: function() {
    return {
      objectHash: null,
      uuid: 0,
      cTab: 'cTab'+this._uid,
      rTab: 'rTab'+this._uid,
      sanctionOutcomeKey: 'sanctionOutcome' + this._uid,
      dtHeadersRelatedItems: [
          'Number',
          'Type',
          'Description',
          'Action',
      ],
      dtOptionsRelatedItems: {
          columns: [
              {
                  data: 'identifier',
              },
              {
                  data: 'model_name',
              },
              {
                  data: 'descriptor',
              },
              {
                  data: 'Action',
                  mRender: function(data, type, row){
                      // return '<a href="#" class="remove_button" data-offender-id="' + row.id + '">Remove</a>';
                      return '<a href="#">View (not implemented)</a>';
                  }
              },
          ]
      },
      disabledDates: {
        from: new Date(),
      },
      workflow_type: '',
      lovCollection : {},
      // get rid of these
      classification_types: [],
      call_types: [],
      wildcare_species_types: [],
      filter_wildcare_species_types: [],
      wildcare_species_sub_types: [],
      filter_wildcare_species_sub_types: [],
      //
      speciesSubTypeDisabled: false,
      isFemalePinkyJoey: false,
      entangled_choices: [],
      gender_choices: [],
      baby_kangaroo_choices: [],
      age_choices: [],
      report_types: [],
      referrers: [],
      referrersSelected: [],
      //allocated_group: [],
      current_schema: [],
      // regionDistricts: [],
      reportAdviceUrl: '',
      sectionLabel: "Details",
      sectionIndex: 1,
      pBody: "pBody" + this._uid,
      loading: [],
      renderer_form: null,
      callemailTab: "callemailTab" + this._uid,
      comms_url: helpers.add_endpoint_json(
        api_endpoints.call_email,
        this.$route.params.call_email_id + "/comms_log"
      ),
      comms_add_url: helpers.add_endpoint_json(
        api_endpoints.call_email,
        this.$route.params.call_email_id + "/add_comms_log"
      ),
      logs_url: helpers.add_endpoint_json(
        api_endpoints.call_email,
        this.$route.params.call_email_id + "/action_log"
      ),
      workflowBindId: '',
      sanctionOutcomeInitialised: false,
      offenceInitialised: false,
      inspectionInitialised: false,
      legalCaseInitialised: false,
      hashAttributeWhitelist: [
          "allocated_group_id",
          "location",
          "location_id",
          "classification",
          "classification_id",
          "call_type",
          "call_type_id",
          "lodgement_date",
          "number",
          "caller",
          "report_type_id",
          "caller_phone_number",
          "anonymous_call",
          "caller_wishes_to_remain_anonymous",
          "occurrence_from_to",
          "occurrence_date_from",
          "occurrence_time_start",
          "occurrence_date_to",
          "occurrence_time_end",
          "date_of_call",
          "time_of_call",
          "advice_given",
          "advice_details",
          "region_id",
          "district_id",
          "case_priority_id",
          "dead",
          "euthanise",
          "number_of_animals",
          "brief_nature_of_call",
          ]
    };
  },
  components: {
    CommsLogs,
    FormSection,
    MapLocation,
    SearchPersonOrganisation,
    CallWorkflow,
    Offence,
    //datatable,
    RelatedItems,
    SanctionOutcome,
    Inspection,
    CreateLegalCaseModal,
  },
  computed: {
    ...mapGetters('callemailStore', {
      call_email: "call_email",
    }),
    ...mapGetters({
      renderer_form_data: 'renderer_form_data',
      //current_user: 'current_user',
    }),
    locationExists: function() {
        if (this.call_email && 
            this.call_email.location && 
            this.call_email.location.geometry && 
            this.call_email.location.geometry.coordinates.length > 0) {
            return true;
        }
    },
    assignToVisible: function() {
        let visible = false;
        if (this.call_email && this.call_email.allocated_group && this.call_email.can_user_action && this.statusId ==='open') {
            visible = true;
        }
        return visible;
    },
    personSearchVisibility: function() {
        let visible = false;
        if (this.statusId ==='open') {
            visible = true;
        }
        return visible;
    },
    closeButtonVisibility: function() {
        let visibility = true;
        if (['closed', 'pending_closure'].includes(this.statusId)) {
            visibility = false;
        }
        return visibility;
    },
    updateSearchPersonOrganisationBindId: function() {
        let bindId = 'individual';
        if (this.call_email.email_user && this.call_email.email_user.id) {
            bindId += this.call_email.email_user.id;
        } else {
            bindId += '0'
        }
        return bindId
    },
    csrf_token: function() {
      return helpers.getCookie("csrftoken");
    },
    callerEntity: function() {
        let entity = {};
        if (this.call_email.email_user && this.call_email.email_user.id) {
            entity.id = this.call_email.email_user.id;
            entity.data_type = 'individual';
        }
        return entity;
    },
    occurrenceDateLabel: function() {
      if (this.call_email.occurrence_from_to) {
        return "Occurrence date from";
      } else {
        return "Occurrence date";
      }
    },
    occurrenceTimeLabel: function() {
      if (this.call_email.occurrence_from_to) {
        return "Occurrence time from";
      } else {
        return "Occurrence time";
      }
    },
    readonlyForm: function() {
        if (this.call_email.id) {
            return !this.call_email.can_user_edit_form;
        } else {
            return true;
        }
    },
    canUserAction: function() {
        return this.call_email.can_user_action;
    },
    statusDisplay: function() {
      return this.call_email.status ? this.call_email.status.name : '';
    },
    statusId: function() {
      return this.call_email.status ? this.call_email.status.id : '';
    },
    offenceExists: function() {
        for (let item of this.call_email.related_items) {
            if (item.model_name.toLowerCase() === "offence") {
                return true
            }
        }
        // return false if no related item is an Offence
        return false
    },
    relatedItemsBindId: function() {
        let timeNow = Date.now()
        if (this.call_email && this.call_email.id) {
            return 'call_email_' + this.call_email.id + '_' + this._uid;
        } else {
            return timeNow.toString();
        }
    },
    relatedItemsVisibility: function() {
        if (this.call_email && this.call_email.id) {
            return true;
        } else {
            return false;
        }
    },
    rendererVisibility: function() {
        if (this.call_email.id && this.current_schema && this.current_schema.length > 0) {
            return true;
        } else {
            return false
        }
    },
    offenceBindId: function() {
        //this.uuid += 1
        return 'offence' + this.uuid;
    },
    isEntangledOther: function() {
        let entangled_other_checked=false;
        if(this.call_email && this.call_email.entangled){
          for (let choice of this.call_email.entangled){
            if(choice === "other")
              entangled_other_checked = true;
          }
        } else{
          entangled_other_checked = false;
        }
        if (entangled_other_checked===false) {
          this.call_email.entangled_other=null;
        }
        return entangled_other_checked;
    },
  },
  filters: {
    formatDate: function(data) {
      return data ? moment(data).format("DD/MM/YYYY HH:mm:ss") : "";
    }
  },
  methods: {
    ...mapActions('callemailStore', {
      loadCallEmail: 'loadCallEmail',
      saveCallEmail: 'saveCallEmail',
      setCallEmail: 'setCallEmail', 
      setRegionId: 'setRegionId',
      setAllocatedGroupList: 'setAllocatedGroupList',
      setOccurrenceTimeStart: 'setOccurrenceTimeStart',
      setOccurrenceTimeEnd: 'setOccurrenceTimeEnd',
      setTimeOfCall: 'setTimeOfCall',
      setDateOfCall: 'setDateOfCall',
      setRelatedItems: 'setRelatedItems',
      setCaller: 'setCaller',
    }),
    ...mapActions({
      saveFormData: 'saveFormData',
    }),
    updateUuid: function() {
        this.uuid += 1;
    },
    entitySelected: async function(para) {
        await this.setCaller(para);
    },
    loadReportAdviceUrl: function(url) {
        if (!this.reportAdviceUrl && this.call_email && this.call_email.report_type) {
            this.reportAdviceUrl = url;
        }
    },

    formChanged: function(){
        let changed = false;
        let copiedCallEmail = {};
        Object.getOwnPropertyNames(this.call_email).forEach(
            (val, idx, array) => {
                if (this.hashAttributeWhitelist.includes(val)) {
                    copiedCallEmail[val] = this.call_email[val]
                }
            });
        this.addHashAttributes(copiedCallEmail);
        if(this.objectHash !== hash(copiedCallEmail)){
            changed = true;
        }
        return changed;
    },
    calculateHash: function() {
        let copiedCallEmail = {}
        Object.getOwnPropertyNames(this.call_email).forEach(
            (val, idx, array) => {
                if (this.hashAttributeWhitelist.includes(val)) {
                    copiedCallEmail[val] = this.call_email[val]
                }
            });
        this.addHashAttributes(copiedCallEmail);
        this.objectHash = hash(copiedCallEmail);
    },
    addHashAttributes: function(obj) {
        let copiedRendererFormData = Object.assign({}, this.renderer_form_data);
        obj.renderer_form_data = copiedRendererFormData;
        let copiedCallerEntity = Object.assign({}, this.callerEntity);
        obj.callerEntity = copiedCallerEntity;
    },
    updateWorkflowBindId: function() {
        let timeNow = Date.now()
        if (this.workflow_type) {
            this.workflowBindId = this.workflow_type + '_' + timeNow.toString();
        } else {
            this.workflowBindId = timeNow.toString();
        }
    },
    async addWorkflow(workflow_type) {
      if (!this.locationExists) {
            await swal({
                title: 'Mandatory Field',
                html: "Location must be specified",
                type: "error",
            })
      } else {
          try {
              const res = await this.saveCallEmail({ crud: 'forward', internal: true });
              if (res.ok) {
                  this.workflow_type = workflow_type;
                  this.updateWorkflowBindId();
                  this.$nextTick(() => {
                    this.$refs.add_workflow.isModalOpen = true;
                  });
              }
          } catch (err) {
          }
      }
    },
    openSanctionOutcome(){
      this.sanctionOutcomeInitialised = true;
      this.$nextTick(() => {
          this.$refs.sanction_outcome.isModalOpen = true;
      });
    },
    openOffence(){
      this.offenceInitialised = true;
      this.$refs.offence.isModalOpen = true;
    },
    allocateForInspection() {
      this.inspectionInitialised = true;
        this.$nextTick(() => {
          this.$refs.inspection.isModalOpen = true
      });
    },
    allocateForLegalCase() {
      this.legalCaseInitialised = true;
        this.$nextTick(() => {
          this.$refs.legal_case.isModalOpen = true
      });
    },
    filterWildcareSpeciesType: function(event,all_wildcare_species) {
      this.$nextTick(() => {
        if(event){
          this.call_email.species_name=null;
          this.call_email.wildcare_species_type_id=null; //-----to remove the previous selection
        }
        this.filter_wildcare_species_types=[];
        this.filter_wildcare_species_types=[{
          id:null,
          display:"",
          call_type_id:null,
          check_pinky_joey:false,
          show_species_name_textbox:false,
        }];
        this.filter_wildcare_species_sub_types=[];
        //------show dependent species for call_type selected
        if(all_wildcare_species === false)
        {
          for(let choice of this.wildcare_species_types){
            if(choice.call_type_id === this.call_email.call_type_id || choice.call_type_id === null)
            {
              this.filter_wildcare_species_types.push(choice);
            }
          }
        }
        else
        {
          this.filter_wildcare_species_types=this.wildcare_species_types; //------else show all species
        }
        //---to reset pinky/Joey onchange of call type
        this.checkFemalePinkyJoey();
      });
    },
    filterWildcareSpeciesSubType: function(event) {
      this.$nextTick(() => {
        if(event){
          this.call_email.species_name=null;
          this.call_email.wildcare_species_sub_type_id=null; //-----to remove the previous selection
        }
        this.filter_wildcare_species_sub_types=[{
          id:null,
          display:"",
          wildcare_species_type_id:null,
        }];
        //---to disable sub type and show species name textbox if 'Other' is selected
        this.speciesSubTypeDisabled = false;
        if(this.readonlyForm)
        {
          this.speciesSubTypeDisabled = true;
        }
        else if(this.call_email.wildcare_species_type_id){
          for(let choice of this.filter_wildcare_species_types){
            if(choice.id === this.call_email.wildcare_species_type_id && choice.show_species_name_textbox === true){
              this.speciesSubTypeDisabled=true;
            }
          }
        }
        //---filter wildcare species sub type as per species type selected
          /*
        if(this.speciesSubTypeDisabled === false)
        {
        */
          for(let choice of this.wildcare_species_sub_types){
            if(choice.wildcare_species_type_id === this.call_email.wildcare_species_type_id)
            {
              this.filter_wildcare_species_sub_types.push(choice);
            }
          }
          /*
        }
        */
        //---to reset pinky/Joey onchange of species type
        this.checkFemalePinkyJoey();
      });
    },
    checkFemalePinkyJoey: function() {
      this.isFemalePinkyJoey=false;
      if(this.call_email && this.call_email.gender.includes("female") && this.call_email.wildcare_species_type_id){
        for(let choice of this.filter_wildcare_species_types){
          if(choice.id === this.call_email.wildcare_species_type_id && choice.check_pinky_joey === true){
            this.isFemalePinkyJoey=true;
          }
        }
      }
      //---to reset pinky/joey if uncheck female
      if (!this.isFemalePinkyJoey) {
        this.call_email.baby_kangaroo=[];
      }
    },
    //saveIndividual: function() {
    //  let noPersonSave = true;
    //  this.save(noPersonSave)
    //},
    save: async function (returnToDash) {
        let savedCallEmail = null;
        let savedPerson = null;
        if (this.call_email.id) {
            if (this.$refs.search_person_organisation && this.$refs.search_person_organisation.entityIsPerson) {
                savedPerson = await this.$refs.search_person_organisation.parentSave()
                // if person save ok, continue with Inspection save
                if (savedPerson && savedPerson.ok) {
                    savedCallEmail = await this.saveCallEmail({ crud: 'save' });
                }
            // no search_person_org
            } else {
                savedCallEmail = await this.saveCallEmail({ crud: 'save' });
            }
        } else {
            // new CallEmail
            savedCallEmail = await this.saveCallEmail({ crud: 'create'});
        }
        // recalc hash after save
        this.calculateHash();
        if (savedCallEmail && savedCallEmail.ok && returnToDash === 'exit') {
            // remove redundant eventListeners
            window.removeEventListener('beforeunload', this.leaving);
            window.removeEventListener('onblur', this.leaving);
            // return to dash
            this.$router.push({ name: 'internal-call-email-dash' });
        }
    },
    duplicate: async function() {
      await this.saveCallEmail({ route: false, crud: 'duplicate'});
    },
    loadSchema: function() {
      if (this.call_email.report_type_id) {
          this.$nextTick(async function() {
              let url = helpers.add_endpoint_json(
                            api_endpoints.report_types,
                            this.call_email.report_type_id + '/get_schema',
                            );
              let returnedData = await Vue.http.get(url);
              let returnedSchema = returnedData.body.schema;
              let returnedAdviceUrl = returnedData.body.adviceurl;
              /*
              let returned_schema = await cache_helper.getSetCache(
                'CallEmail_ReportTypeSchema', 
                this.call_email.id.toString(), 
                url);
              */
              if (returnedSchema) {
                this.current_schema = returnedSchema;
              }
              if (returnedAdviceUrl) {
                  this.reportAdviceUrl = returnedAdviceUrl;
              }
          });
      } else {
          this.current_schema = [];
      }
    },
    updateAssignedToId: async function (user) {
        let url = helpers.add_endpoint_join(
            api_endpoints.call_email, 
            this.call_email.id + '/update_assigned_to_id/'
            );
        let payload = null;
        if (user === 'current_user' && this.call_email.user_in_group) {
            payload = {'current_user': true};
        } else if (user === 'blank') {
            payload = {'blank': true};
        } else {
            payload = { 'assigned_to_id': this.call_email.assigned_to_id };
        }
        let res = await Vue.http.post(
            url,
            payload
        );
        await this.setCallEmail(res.body); 
    },
    addEventListeners: function() {
      let vm = this;
      let el_fr_date = $(vm.$refs.occurrenceDateFromPicker);
      let el_fr_time = $(vm.$refs.occurrenceTimeFromPicker);
      let el_to_date = $(vm.$refs.occurrenceDateToPicker);
      let el_to_time = $(vm.$refs.occurrenceTimeToPicker);
      let el_date_of_call = $(vm.$refs.dateOfCallPicker);
      let el_time_of_call = $(vm.$refs.timeOfCallPicker);

      // "From" field
      el_fr_date.datetimepicker({
        format: "DD/MM/YYYY",
        maxDate: "now",
        showClear: true
      });
      el_fr_date.on("dp.change", function(e) {
        if (el_fr_date.data("DateTimePicker").date()) {
          vm.call_email.occurrence_date_from = e.date.format("DD/MM/YYYY");
        } else if (el_fr_date.data("date") === "") {
          vm.call_email.occurrence_date_from = "";
        }
      });
      el_fr_time.datetimepicker({ format: "LT", showClear: true });
      el_fr_time.on("dp.change", function(e) {
        if (el_fr_time.data("DateTimePicker").date()) {
          vm.call_email.occurrence_time_from = e.date.format("LT");
        } else if (el_fr_time.data("date") === "") {
          vm.call_email.occurrence_time_from = "";
        }
      });

      // "To" field
      el_to_date.datetimepicker({
        format: "DD/MM/YYYY",
        maxDate: "now",
        showClear: true
      });
      el_to_date.on("dp.change", function(e) {
        if (el_to_date.data("DateTimePicker").date()) {
          vm.call_email.occurrence_date_to = e.date.format("DD/MM/YYYY");
        } else if (el_to_date.data("date") === "") {
          vm.call_email.occurrence_date_to = "";
        }
      });
      el_to_time.datetimepicker({ format: "LT", showClear: true });
      el_to_time.on("dp.change", function(e) {
        if (el_to_time.data("DateTimePicker").date()) {
          vm.call_email.occurrence_time_to = e.date.format("LT");
        } else if (el_to_time.data("date") === "") {
          vm.call_email.occurrence_time_to = "";
        }
      });
      // Date/Time of call
      el_date_of_call.datetimepicker({
        format: "DD/MM/YYYY",
        maxDate: "now",
        //useCurrent: true,
        //showClear: true
      });
      el_date_of_call.on("dp.change", function(e) {
        if (el_date_of_call.data("DateTimePicker").date()) {
          vm.call_email.date_of_call = e.date.format("DD/MM/YYYY");
        } else if (el_date_of_call.data("date") === "") {
          vm.call_email.date_of_call = "";
        }
      });
      el_time_of_call.datetimepicker({ format: "LT", showClear: true });
      el_time_of_call.on("dp.change", function(e) {
        if (el_time_of_call.data("DateTimePicker").date()) {
          vm.call_email.time_of_call = e.date.format("LT");
        } else if (el_time_of_call.data("date") === "") {
          vm.call_email.time_of_call = "";
        }
      });
      window.addEventListener('beforeunload', this.leaving);
      window.addEventListener('onblur', this.leaving);
    },
    leaving: function(e) {
        //let vm = this;
        let dialogText = 'You have some unsaved changes.';
        if (this.formChanged()){
            e.returnValue = dialogText;
            return dialogText;
        }
    },
  },
  destroyed: function() {
      window.removeEventListener('beforeunload', this.leaving);
      window.removeEventListener('onblur', this.leaving);
  },
  created: async function() {
    if (this.$route.params.call_email_id) {
      await this.loadCallEmail({ call_email_id: this.$route.params.call_email_id });
    }
    // await this.loadComplianceAllocatedGroup(this.call_email.allocated_group_id);
    // load drop-down select lists
    
    /// large LOV(List Of Values) object
    const lovResponse = await Vue.http.get('/api/lov_collection/lov_collection_choices/');
    this.lovCollection = lovResponse.body;

    // classification_types
    //let returned_classification_types = await Vue.http.get('/api/classification/classification_choices/');
    Object.assign(this.classification_types, this.lovCollection.classification_types);
    // call_types
    //let returned_call_types = await Vue.http.get('/api/call_type/call_type_choices/');
    Object.assign(this.call_types, this.lovCollection.call_type_choices);
    //Wildcare Species Types
    //let returned_wildcare_species_types = await Vue.http.get('/api/wildcare_species_type/wildcare_species_type_choices/');
    Object.assign(this.wildcare_species_types, this.lovCollection.wildcare_species_types);
    //Wildcare Species Sub Types
    //let returned_wildcare_species_sub_types = await Vue.http.get('/api/wildcare_species_sub_type/wildcare_species_sub_type_choices/');
    Object.assign(this.wildcare_species_sub_types, this.lovCollection.wildcare_species_sub_types);
    // Entangled choices
    //let returned_entangled_choices = await Vue.http.get('/api/call_email/entangled_choices/');
    Object.assign(this.entangled_choices, this.lovCollection.entangled_choices);
    // Gender choices
    //let returned_gender_choices = await Vue.http.get('/api/call_email/gender_choices/');
    Object.assign(this.gender_choices, this.lovCollection.gender_choices);
    // Pinky/Joey choices
    //let returned_baby_kangaroo_choices = await Vue.http.get('/api/call_email/baby_kangaroo_choices/');
    Object.assign(this.baby_kangaroo_choices, this.lovCollection.baby_kangaroo_choices);
    // Age choices
    //let returned_age_choices = await Vue.http.get('/api/call_email/age_choices/');
    Object.assign(this.age_choices, this.lovCollection.age_choices);
    //report_types
    let returned_report_types = await cache_helper.getSetCacheList('CallEmail_ReportTypes', helpers.add_endpoint_json(
                    api_endpoints.report_types,
                    'get_distinct_queryset'));
    Object.assign(this.report_types, returned_report_types);
    // blank entry allows user to clear selection
    this.report_types.splice(0, 0, 
      {
        id: "", 
        name: "",
      });
    // referrers
    let returned_referrers = await cache_helper.getSetCacheList('CallEmail_Referrers', '/api/referrers.json');
    Object.assign(this.referrers, returned_referrers);
    // blank entry allows user to clear selection
    this.referrers.splice(0, 0, 
      {
        id: "", 
        name: "",
      });

     // load selected referrers into local var
    for (let referrer_id of this.call_email.selected_referrers) {
        this.referrersSelected.push(referrer_id)
    }
    //Object.assign(this.referrersSelected, this.call_email.selected_referrers)

    // load current CallEmail renderer schema
    if (this.call_email && this.call_email.report_type_id) {
      await this.loadSchema();
    }
    if (this.call_email && this.call_email.report_type && this.call_email.report_type.advice_url) {
        this.loadReportAdviceUrl(this.call_email.report_type.advice_url);
    }

    // regionDistricts
    // let returned_region_districts = await cache_helper.getSetCacheList(
    //   'RegionDistricts', 
    //   api_endpoints.region_district
    //   );
    // Object.assign(this.regionDistricts, returned_region_districts);
    
    // Apply current timestamp to date and time of call
    if (!this.call_email.date_of_call && this.call_email.can_user_edit_form) {
        this.setDateOfCall(moment().format('DD/MM/YYYY'));
    }
    if (!this.call_email.time_of_call && this.call_email.can_user_edit_form) {
        this.setTimeOfCall(moment().format('LT'));
    }
    this.calculateHash();
    this.filterWildcareSpeciesType();
    this.$nextTick(function() {
        this.filterWildcareSpeciesSubType();
        this.checkFemalePinkyJoey();
    });
  },
  mounted: function() {
      let vm = this;
      $( 'a[data-toggle="collapse"]' ).on( 'click', function () {
          var chev = $( this ).children()[ 0 ];
          window.setTimeout( function () {
              $( chev ).toggleClass( "glyphicon-chevron-down glyphicon-chevron-up" );
          }, 100 );
      });
      // Time field controls
      $('#occurrenceTimeStartPicker').datetimepicker({
              format: 'LT'
          });
      $('#occurrenceTimeEndPicker').datetimepicker({
              format: 'LT'
          });
      $('#occurrenceTimeStartPicker').on('dp.change', function(e) {
          vm.setOccurrenceTimeStart(e.date.format('LT'));
      });
      $('#occurrenceTimeEndPicker').on('dp.change', function(e) {
          vm.setOccurrenceTimeEnd(e.date.format('LT'));
      }); 
      $('#timeOfCallPicker').datetimepicker({
              format: 'LT'
          });
      $('#timeOfCallPicker').on('dp.change', function(e) {
          vm.setTimeOfCall(e.date.format('LT'));
      }); 
      vm.$nextTick(() => {
          vm.addEventListeners();
          //this.calculateHash();
      });

  }
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
.advice-url-label {
  visibility: hidden;
}
.advice-url {
  padding-left: 20%;
}
</style>
