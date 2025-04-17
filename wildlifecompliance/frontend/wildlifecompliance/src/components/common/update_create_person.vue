<template lang="html">
    <div :id="elementId">
        <div class="col-sm-12">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h3 class="panel-title">Personal Details
                        <span class="glyphicon  pull-right" @click="isPersonalDetailsOpen=!isPersonalDetailsOpen" :class="isPersonalDetailsOpen ? 'glyphicon-chevron-up' : 'glyphicon-chevron-down'"></span>
                    </h3>
                </div>
                <div class="panel-body in" :id="pdBody">
                    <div v-if="objectAlert" class="alert alert-danger">
                        <p>test alert</p>
                    </div>
                    <form class="form-horizontal" name="personal_form" method="post">
                        <div class="form-group" v-bind:class="{ 'has-error': errorGivenName }">
                            <label for="" class="col-sm-3 control-label">Given Name(s)</label>
                            <div class="col-sm-6">
                                <div v-if="email_user">
                                    <input :readonly="personalDetailsReadOnly" type="text" class="form-control" name="first_name" placeholder="" v-model="email_user.first_name" v-bind:key="email_user.id">
                                </div>
                            </div>
                        </div>
                        <div class="form-group" v-bind:class="{ 'has-error': errorLastName }">
                            <label for="" class="col-sm-3 control-label">Last Name</label>
                            <div class="col-sm-6">
                                <div v-if="email_user">
                                    <input :readonly="personalDetailsReadOnly" type="text" class="form-control" name="last_name" placeholder="" v-model="email_user.last_name" v-bind:key="email_user.id">
                                </div>
                            </div>
                        </div>
                        <div v-if="email_user" class="form-group" v-bind:class="{ 'has-error': errorDob }">
                            <label for="" class="col-sm-3 control-label" >Date of Birth</label>
                            <div class="col-sm-6">
                                <div class="input-group date" ref="dobDatePicker">
                                    <input 
                                    :disabled="personalDetailsReadOnly" 
                                    type="text" 
                                    class="form-control" 
                                    placeholder="DD/MM/YYYY" 
                                    v-model="email_user.dob" 
                                     />
                                    <span class="input-group-addon">
                                        <span class="glyphicon glyphicon-calendar"></span>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>

            <div class="panel panel-default">
                <div class="panel-heading">
                <h3 class="panel-title">Address Details
                    <span class="glyphicon  pull-right" @click="isAddressDetailsOpen=!isAddressDetailsOpen" :class="isAddressDetailsOpen ? 'glyphicon-chevron-up' : 'glyphicon-chevron-down'"></span>
                </h3>
                </div>
                <div class="panel-body in" :id="adBody">
                    <form class="form-horizontal" action="index.html" method="post">
                        <div class="form-group">
                        <label for="" class="col-sm-3 control-label">Street</label>
                        <div class="col-sm-6">
                            <div v-if="email_user"><div>
                                <input :readonly="!isEditable" type="text" class="form-control" name="street" placeholder="" v-model="email_user.residential_address.line1" v-bind:key="email_user.residential_address.id">
                            </div></div>
                        </div>
                        </div>
                    <div class="form-group">
                        <label for="" class="col-sm-3 control-label" >Town/Suburb</label>
                        <div class="col-sm-6">
                            <div v-if="email_user"><div>
                                <input :readonly="!isEditable" type="text" class="form-control" name="surburb" placeholder="" v-model="email_user.residential_address.locality" v-bind:key="email_user.residential_address.id">
                            </div></div>
                        </div>
                        </div>
                        <div class="form-group">
                        <label for="" class="col-sm-3 control-label">State</label>
                        <div class="col-sm-2">
                            <div v-if="email_user"><div>
                                <input :readonly="!isEditable" type="text" class="form-control" name="country" placeholder="" v-model="email_user.residential_address.state" v-bind:key="email_user.residential_address.id">
                            </div></div>
                        </div>
                        <label for="" class="col-sm-2 control-label">Postcode</label>
                        <div class="col-sm-2">
                            <div v-if="email_user"><div>
                                <input :readonly="!isEditable" type="text" class="form-control" name="postcode" placeholder="" v-model="email_user.residential_address.postcode" v-bind:key="email_user.residential_address.id">
                            </div></div>
                        </div>
                        </div>
                        <div class="form-group">
                        <label for="" class="col-sm-3 control-label" >Country</label>
                        <div class="col-sm-4">
                            <div v-if="email_user"><div>
                                <select :disabled="!isEditable" class="form-control" name="country" v-model="email_user.residential_address.country" v-bind:key="email_user.residential_address.id">
                                    <option v-for="c in countries" :value="c.code">{{ c.name }}</option>
                                </select>
                            </div></div>
                        </div>
                        </div>
                    </form>
                </div>
            </div>

            <div class="panel panel-default">
                <div class="panel-heading">
                <h3 class="panel-title">Contact Details <small></small>
                    <span class="glyphicon  pull-right" @click="isContactDetailsOpen=!isContactDetailsOpen" :class="isContactDetailsOpen ? 'glyphicon-chevron-up' : 'glyphicon-chevron-down'"></span>
                </h3>
                </div>
                <div class="panel-body collapse in" :id="cdBody">
                    <form class="form-horizontal" action="index.html" method="post">
                        <div class="form-group">
                        <label for="" class="col-sm-3 control-label">Phone</label>
                        <div class="col-sm-6">
                            <div v-if="email_user">
                                <input :readonly="!isEditable" type="text" class="form-control" name="phone" placeholder="" v-model="email_user.phone_number" v-bind:key="email_user.id">
                            </div>
                        </div>
                        </div>
                        <div class="form-group">
                        <label for="" class="col-sm-3 control-label" >Mobile</label>
                        <div class="col-sm-6">
                            <div v-if="email_user">
                                <input :readonly="!isEditable" type="text" class="form-control" name="mobile" placeholder="" v-model="email_user.mobile_number" v-bind:key="email_user.id">
                            </div>
                        </div>
                        </div>
                        <div class="form-group">
                        <label for="" class="col-sm-3 control-label" >Email</label>
                        <div class="col-sm-6">
                            <div v-if="email_user">
                                <input :readonly="!isEditable" type="email" class="form-control" name="email" placeholder="" v-model="email_user.email" v-bind:key="email_user.id"> </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>

            <input 
            :disabled="!saveButtonEnabled"
            type="button" 
            class="pull-right btn btn-primary" 
            :value="saveButtonText" 
            @click.prevent="saveData" />
        </div>
    </div>
</template>

<script>
import Vue from 'vue';
import $ from "jquery";
import { api_endpoints, helpers } from '@/utils/hooks'
import utils from '../internal/utils'
//import "bootstrap/dist/css/bootstrap.css"
//import 'eonasdan-bootstrap-datetimepicker';
//import moment from 'moment'

export default {
    name: "update-create-person",

    data: function(){
        let vm = this;

        return {
            mainElement: null,
            elementId: 'create_new_person_' + vm._uid,

            pdBody: 'pdBody'+vm._uid,
            cdBody: 'cdBody'+vm._uid,
            adBody: 'adBody'+vm._uid,
            errorGivenName: false,
            errorLastName: false,
            errorDob: false,
            objectAlert: false,
            loading: [],
            countries: [],
            saveButtonEnabled: false,

            // New toggles
            isPersonalDetailsOpen: null,
            isAddressDetailsOpen: null,
            isContactDetailsOpen: null,

            email_user : {
                id: null,
                first_name: '',
                last_name: '',
                dob: null,
                residential_address: {
                    line1: '',
                    locality: '',
                    state: 'WA',
                    postcode: '',
                    country: 'AU'
                },
                phone_number: '',
                mobile_number: '',
                email: '',
            }
        }
    },
    props: {
        displayComponent: {
            type: Boolean,
            required: true,
            default: false,
        },
        displaySaveButton: {
            type: Boolean,
            required: false,
            default: true,
        },
        defaultOpenPersonalDetails: {
            type: Boolean,
            required: false,
            default: true,
        },
        defaultOpenAddressDetails: {
            type: Boolean,
            required: false,
            default: false,
        },
        defaultOpenContactDetails: {
            type: Boolean,
            required: false,
            default: false,
        },
        slideDownMiliSecond: {
            type: Number,
            required: false,
            default: 200,
        },
        slideUpMiliSecond: {
            type: Number,
            required: false,
            default: 300,
        },
        personToUpdate: {
            type: Number,
            required: false,
        },
        isEditable: {
            type: Boolean,
            default: false,
        },
    },
    computed: {
        personId: function() {
            return this.email_user.id;
        },
        personalDetailsReadOnly: function() {
            if (this.email_user.id) {
                return true;
            }
        },
        computedEmailUser: function() {
            let computedUser = Object.assign({}, this.email_user);
            if (this.email_user && this.email_user.residential_address) {
                Object.assign(computedUser.residential_address, this.email_user.residential_address);
            }
            return computedUser;
        },
        saveButtonText: function() {
            let buttonText = '';
            if (this.email_user && this.email_user.id) {
                buttonText = 'Update Person'
            } else {
                buttonText = 'Save New Person'
            }
            return buttonText;
        },

    },
    watch: {
        displayComponent: {
            handler: function() {
                this.showHideElement();
            }
        },
        isPersonalDetailsOpen: {
            handler: function(){
                let elem = $('#' + this.pdBody);
                if(this.isPersonalDetailsOpen) {
                    elem.slideDown(this.slideDownMiliSecond);
                } else {
                    elem.slideUp(this.slideUpMiliSecond);
                }
            }
        },
        isAddressDetailsOpen: {
            handler: function(){
                let elem = $('#' + this.adBody);
                if(this.isAddressDetailsOpen) {
                    elem.slideDown(this.slideDownMiliSecond);
                } else {
                    elem.slideUp(this.slideUpMiliSecond);
                }
            }
        },
        isContactDetailsOpen: {
            handler: function(){
                let elem = $('#' + this.cdBody);
                if(this.isContactDetailsOpen) {
                    elem.slideDown(this.slideDownMiliSecond);
                } else {
                    elem.slideUp(this.slideUpMiliSecond);
                }
            }
        },
        computedEmailUser: {
            deep: true,
            handler: function(newVal, oldVal) {
                if (oldVal.id && oldVal !== newVal) {
                    this.saveButtonEnabled = true;
                } else if (this.email_user && !this.email_user.id) {
                    this.saveButtonEnabled = true;
                } else {
                    this.saveButtonEnabled = false;
                }
            },
        },

    },
    methods: {
        addEventListeners: function() {
          //let vm = this;
          let el_fr_date = $(this.$refs.dobDatePicker);
          //let el_fr_time = $(vm.$refs.plannedForTimePicker);

          // "From" field
          el_fr_date.datetimepicker({
            format: "DD/MM/YYYY",
            maxDate: "now",
            showClear: true
          });
          el_fr_date.on("dp.change", (e) => {
            if (el_fr_date.data("DateTimePicker").date()) {
              this.email_user.dob = e.date.format("DD/MM/YYYY");
            } else if (el_fr_date.data("date") === "") {
              this.email_user.dob = "";
            }
          });
        },
        setExistingPerson: function(id){
            //let vm = this;

            let initialisers = [utils.fetchUser(id)];
            Promise.all(initialisers).then((data) => {
                Object.assign(this.email_user, data[0])
                if (!this.email_user.residential_address) {
                    this.email_user.residential_address = this.getDefaultAddress()
                }
                if (this.email_user.dob) {
                    this.email_user.dob = moment(this.email_user.dob, 'YYYY-MM-DD').format('DD/MM/YYYY');
                }
            });
        },
        setPersonId: function(id){
            this.email_user.id = id;
        },
        setDefaultPerson: function(){
            let user_data = {
                id: null,
                first_name: '',
                last_name: '',
                dob: null,
                residential_address: {
                    line1: '',
                    locality: '',
                    state: 'WA',
                    postcode: '',
                    country: 'AU'
                },
                phone_number: '',
                mobile_number: '',
                email: '',
            };
            Object.assign(this.email_user, user_data);
        },
        getDefaultAddress: function(){
            let residential_address_data = {
                    line1: '',
                    locality: '',
                    state: 'WA',
                    postcode: '',
                    country: 'AU'
                };
            return residential_address_data;
        },
        handleSlideElement: function(elem_id){
            let elem = $('#' + elem_id);
            if (keyword == 'pd'){
                this.isPersonalDetailsOpen = !this.isPersonalDetailsOpen;
            } else if (keyword == 'ad'){
                this.isAddressDetailsOpen = !this.isAddressDetailsOpen;
            } else if (keyword == 'cd') {
                this.isContactDetailsOpen = !this.isContactDetailsOpen;
            }
        },
        loadCountries: function(){
            let vm = this;
            let initialisers = [
                utils.fetchCountries()
            ]
            Promise.all(initialisers).then(data => {
                vm.countries = data[0];
            });
        },
        parentSave: async function() {
            let savedEmailUser = null;
            if (this.saveButtonEnabled) {
                savedEmailUser = await this.saveData('parentSave')
            } else {
                savedEmailUser = {'ok': true};
            }
            return savedEmailUser;
        },
        saveData: async function(parentSave) {
            let savedEmailUser = null;
            try{
                let payload = {}
                Object.assign(payload, this.email_user)
                if (payload.residential_address && !payload.residential_address.line1) {
                    payload.residential_address = null;
                }
                if (payload.dob) {
                    payload.dob = moment(payload.dob, 'DD/MM/YYYY').format('YYYY-MM-DD');
                }
                let fetchUrl = ''
                if (payload.id) {
                    if (!payload.email) {
                        await swal("Error", "Ensure the email field is not blank", "error");
                        return;
                    } else {
                        fetchUrl = helpers.add_endpoint_join(api_endpoints.compliance_management_users, payload.id + '/update_person/');
                    }
                } else {
                    if (!payload.first_name || !payload.last_name || !payload.dob || !payload.email) {
                        await swal("Error", "Fill out all Personal Details and email fields", "error");
                        return;
                    } else {
                        fetchUrl = api_endpoints.compliance_management_users;
                    }
                }

                savedEmailUser = await Vue.http.post(fetchUrl, payload);
                if (!savedEmailUser.body.residential_address) {
                    savedEmailUser.body.residential_address = this.getDefaultAddress()
                }
                Object.assign(this.email_user, savedEmailUser.body);
                this.email_user.dob = moment(this.email_user.dob, 'YYYY-MM-DD').format('DD/MM/YYYY');
                if (!(parentSave === 'parentSave')) {
                    await swal("Saved", "Person has been saved", "success");
                }
                this.$emit('person-saved', {'person': savedEmailUser.body, 'errorMessage': null});
            } catch (err) {
                if (err.bodyText) {
                    await swal("Error", err.bodyText, "error");
                    //this.$emit('person-saved', { 'person': null, 'errorMessage': err.bodyText });
                }
            }
            return savedEmailUser;
        },
        showHideElement: function() {
            if(this.displayComponent) {
                this.mainElement.slideDown(this.slideDownMiliSecond);
            } else {
                this.mainElement.slideUp(this.slideUpMiliSecond);
            }
        }
    },
    mounted: function() {
        let vm = this;
        let elem = document.getElementById(vm.elementId);
        vm.mainElement = $(elem);
        vm.$nextTick(()=>{
            vm.showHideElement();
            vm.loadCountries();

            // Default settings of open / hide
            vm.isPersonalDetailsOpen = vm.defaultOpenPersonalDetails;
            vm.isAddressDetailsOpen = vm.defaultOpenAddressDetails;
            vm.isContactDetailsOpen = vm.defaultOpenContactDetails;
            vm.addEventListeners();
        })
    },
    created: function() {
        if (this.personToUpdate) {
            this.setExistingPerson(this.personToUpdate);
        }
    },
}
</script>

<style>

</style>
