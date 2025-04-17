<template lang="html">
    <div class="">
        <div class="col-sm-12 form-group"><div class="row">
                <label v-if="componentTitle" class="col-sm-4">{{ componentTitle }}</label>
                <label v-else-if="displayTitle" class="col-sm-4">{{ labelTitle }}</label>
                <div v-if="!personOnly">
                    <input :disabled="!isEditable" class="col-sm-1" id="individual" type="radio" v-model="searchType" v-bind:value="`individual`">
                    <label class="col-sm-1" for="individual">Person</label>
                    <input :disabled="!isEditable" class="col-sm-1" id="organisation" type="radio" v-model="searchType" v-bind:value="`organisation`">
                    <label class="col-sm-1" for="organisation">Organisation</label>
                </div>
        </div></div>
        <div class="form-group"><div class="row">
            <div class="col-sm-12">
                <div class="col-sm-9">
                    <input :id="elemId" :class="classNames" :readonly="!isEditable" ref="search_person_org"/>
                </div>
                <div v-if="showCreateNewPerson" class="col-sm-2">
                    <input :disabled="!isEditable" type="button" class="btn btn-primary" value="Create New Person" @click.prevent="createNewPerson()" />
                </div>
                <div v-if="showClearPerson" class="col-sm-2">
                    <input :disabled="!isEditable" type="button" class="btn btn-primary" value="Clear Person" @click.prevent="clearPerson()" />
                </div>
                <div v-else-if="showCreateNewOrganisation" class="col-sm-2">
                    <input :disabled="!isEditable" type="button" class="btn btn-primary" value="Create New Organisation" @click.prevent="createNewOrganisation" />
                </div>
            </div>
        </div></div>
        <div class="form-group"><div class="row">
            <div class="col-sm-12" v-if="displayUpdateCreatePerson">
              <updateCreatePerson 
              displayComponent 
              :isEditable="isEditable"
              :personToUpdate="entity.id"
              @person-saved="savePerson"
              v-bind:key="updateCreatePersonBindId"
              ref="update_create_person"/>
            </div>
            <div class="col-sm-12" v-if="displayUpdateCreateOrganisation && !personOnly">
              <updateCreateOrganisation 
              displayComponent 
              @organisation-saved=""
              ref="update_create_organisation"
              />
            </div>
        </div></div>
    </div>
</template>

<script>
import Awesomplete from "awesomplete";
import $ from "jquery";
//import "bootstrap/dist/css/bootstrap.css";
import "awesomplete/awesomplete.css";
import updateCreatePerson from '@common-components/update_create_person.vue'
import updateCreateOrganisation from '@common-components/update_create_organisation.vue'
import hash from 'object-hash';
import { api_endpoints, helpers, cache_helper } from "@/utils/hooks";

export default {
    name: "search-person-organisation",
    data: function(){
        let vm = this
        vm.awesomplete_obj = null;
        return {
            entity: {
                id: null,
                data_type: null,
                full_name: null,
            },
            displayUpdateCreatePerson: false,
            displayUpdateCreateOrganisation: false,
            searchType: '',
            errorText: '',
            uuid: 0,
            showCreateNewPerson: false,
            showCreateNewOrganisation: false,
            creatingPerson: false,
            creatingOrganisation: false,
            //departmentalStaffList: [],
        }
    },
    components: {
        updateCreatePerson,
        updateCreateOrganisation,
    },
    watch: {
        entity: {
            handler: function (){
                if (this.entity.id) {
                    if (this.addFullName) {
                        console.log('here')
                        this.$emit('entity-selected', {
                            id: this.entity.id,
                            data_type: this.entity.data_type,
                            full_name: this.entity.full_name
                        });
                    } else {
                        console.log('there')
                        this.$emit('entity-selected', {
                            id: this.entity.id, 
                            data_type: this.entity.data_type });
                    }
                }
                if (this.entity.id && this.entity.data_type === 'individual') {
                    this.displayUpdateCreateOrganisation = false;
                    this.displayUpdateCreatePerson = true;
                    this.creatingPerson = false;
                } else if (this.entity.id && this.entity.data_type === 'organisation') {
                    this.displayUpdateCreatePerson = false;
                    // TODO: swap following two lines once create org implemented
                    //this.displayUpdateCreateOrganisation = true;
                    this.displayUpdateCreateOrganisation = false;
                    this.creatingOrganisation = false;
                }
            },
            deep: true
        },
    },
    computed: {
        formChanged: function(){
            let changed = false;
            if(this.object_hash !== hash(this.entity)){
                changed = true;
            }
            return changed;
        },
        elemId: function() {
            this.uuid += 1
            let domId = this.searchType + this.uuid + 'search';

            if (this.domIdHelper) {
                domId += this.domIdHelper;
            }
            return domId;
        },
        labelTitle: function() {
            if (this.searchType) {
                return "Search " + this.searchType;
            }
        },
        updateCreatePersonBindId: function() {
            let bindId = 'person'
            if (this.entity.data_type === 'individual' && this.entity.id) {
                bindId += this.entity.id
            } else {
                bindId += this.uuid;
            }
            return bindId;
        },
        entityIsPerson: function() {
            let check = false;
            if ((this.entity.data_type === 'individual' && this.entity.id) || this.creatingPerson) {
                check = true
            }
            return check;
        },
        entityIsOrganisation: function() {
            let check = false;
            if ((this.entity.data_type === 'organisation' && this.entity.id) || this.creatingOrganisation) {
                check = true
            }
            return check;
        },
    },
    props: {
        showClearPerson: {
            required: false,
            default: false,
        },
        classNames: {
            required: false,
            default: 'form-control',
        },
        maxItems: {
            required: false,
            default: 10
        },
        initialSearchType: {
            required: false,
            default: 'individual' // 'individual' or 'organisation'
                                  //  This variable can be changed dynamically, for example, by the selection of radio buttons
        },
        isEditable: {
            required: false,
            default: true
        },
        excludeStaff: {
            type: Boolean,
            required: false,
            default: false,
        },
        departmentalStaff: {
            type: Boolean,
            required: false,
            default: false,
        },
        showCreateUpdate: {
            type: Boolean,
            required: false,
            default: false,
        },
        parentEntity: {
            type: Object,
            required: false,
        },
        domIdHelper: {
            type: String,
            required: false,
        },
        componentTitle: {
            type: String,
            required: false,
        },
        personOnly: {
            type: Boolean,
            required: false,
            default: false,
        },
        addFullName: {
            type: Boolean,
            required: false,
            default: false,
        },
        displayTitle: {
            type: Boolean,
            required: false,
            default: true,
        },
        entityEdit: {
            type: Object,
            required: false,
        },
    },
    methods: {
        parentSave: async function() {
            let savedEntity = null;
            console.log("parent save")
            if (this.searchType === 'individual') {
                savedEntity = await this.$refs.update_create_person.parentSave()
            } else if (this.searchType === 'organisation') {
                savedEntity = await this.$refs.update_create_organisation.parentSave()
            }
            console.log(savedEntity)
            return savedEntity;
        },
        clearPerson: function() {
            this.$emit('clear-person');
            this.entity = {
                'id': 0, 
                'data_type': 'individual',
                'full_name': '',
            };
            let element_search = $('#' + this.elemId);
            console.log(element_search);
            element_search.val('');
            this.displayUpdateCreatePerson = false;
        },
        createNewPerson: function() {
            this.creatingPerson = true;
            this.entity = {
                id: null,
                data_type: null
            },
            this.$nextTick(() => {
                this.displayUpdateCreatePerson = true;
                this.setInput('');
                if (this.$refs.update_create_person && this.$refs.update_create_person.email_user) {
                    this.$refs.update_create_person.setDefaultPerson();
                    this.$emit('entity-selected', {data_type: 'individual', id: null});
                }
            });
        },
        createNewOrganisation: function() {
            this.creatingOrganisation = true;
            //this.displayUpdateCreateOrganisation = !this.displayUpdateCreateOrganisation;
        },
        clearInput: function(){
            document.getElementById(this.elemId).value = "";
        },
        setInput: function(person_org_str){
            document.getElementById(this.elemId).value = person_org_str;
        },
        markMatchedText(original_text, input) {
            let ret_text = original_text.replace(new RegExp(input, "gi"), function( a, b) {
                return "<mark>" + a + "</mark>";
            });
            return ret_text;
        },
        createUpdateOrganisationClicked: function() {
          this.displayUpdateCreateOrganisation = !this.displayUpdateCreateOrganisation;
        },
        savePerson: async function(obj) {
            if(obj.person){
                if (!obj.updateSearchBox) {
                    await this.$emit('entity-selected', {data_type: 'individual', id: obj.person.id});
                    //await this.$emit('save-individual', {data_type: 'individual', id: obj.person.id});
                }


                // Set fullname and DOB into the input box
                let full_name = [obj.person.first_name, obj.person.last_name].filter(Boolean).join(" ");
                let dob = obj.person.dob ? "DOB:" + obj.person.dob : "DOB: ---";
                let value = [full_name, dob].filter(Boolean).join(", ");
                this.setInput(value);
            } else if (obj.errorMessage) {
                let errorMessage = obj.errorMessage
                await swal("Error", errorMessage, "error");
            }
        },
        initAwesomplete: function() {
            let vm = this;

            let element_search = document.getElementById(vm.elemId);
            vm.awesomplete_obj = new Awesomplete(element_search, {
                maxItems: vm.maxItems,
                sort: false,
                filter: () => {
                    return true;
                }, 
                item: function(text, input) {
                    let ret = Awesomplete.ITEM(text, ""); // Not sure how this works but this doesn't add <mark></mark>
                    return ret;
                },
                data: function(item, input) {
                    if (vm.searchType == "individual") {
                        let f_name = item.first_name ? item.first_name : "";
                        let l_name = item.last_name ? item.last_name : "";
            
                        let full_name = [f_name, l_name].filter(Boolean).join(" ");
                        //console.log(full_name)
                        //let individual_full_name = f_name + ' ' + l_name;
                        let email = item.email ? "E:" + item.email : "";
                        let p_number = item.phone_number ? "P:" + item.phone_number : "";
                        let m_number = item.mobile_number ? "M:" + item.mobile_number : "";
                        let dob = item.dob ? "DOB:" + item.dob : "DOB: ---";
            
                        let full_name_marked = "<strong>" + vm.markMatchedText(full_name, input) + "</strong>";
                        let email_marked = vm.markMatchedText(email, input);
                        let p_number_marked = vm.markMatchedText(p_number, input);
                        let m_number_marked = vm.markMatchedText(m_number, input);
                        let dob_marked = vm.markMatchedText(dob, input);
            
                        let myLabel = [
                            full_name_marked,
                            email_marked,
                            p_number_marked,
                            m_number_marked,
                            dob_marked
                        ].filter(Boolean).join("<br />");
                        myLabel = "<div data-item-id=" + item.id + ' data-full-name="' + full_name + '" data-type="individual">' + myLabel + "</div>";
            
                        return {
                            label: myLabel, // Displayed in the list below the search box
                            value: [full_name, dob].filter(Boolean).join(", "), // Inserted into the search box once selected
                            id: item.id
                        };
                    } else {
                        let name = item.name ? item.name : "";
                        let abn = item.abn ? "ABN:" + item.abn : "";
            
                        let name_marked = "<strong>" + vm.markMatchedText(name, input) + "</strong>";
                        let abn_marked = vm.markMatchedText(abn, input);
            
                        let myLabel = [name_marked, abn_marked].filter(Boolean).join("<br />");
                        myLabel = "<div data-item-id=" + item.id + ' data-type="organisation">' + myLabel + "</div>";
            
                        return {
                            label: myLabel,
                            value: [name, abn].filter(Boolean).join(", "),
                            id: item.id
                        };
                    }
                }
            });
            $(element_search)
            .on("keyup", function(ev) {
                var keyCode = ev.keyCode || ev.which;
                if ((48 <= keyCode && keyCode <= 90) || (96 <= keyCode && keyCode <= 105) || keyCode == 8 || keyCode == 46) {
                    vm.search_person_or_organisation(ev.target.value);
                    return false;
                }
            })
            .on("awesomplete-selectcomplete", function(ev) {
                ev.preventDefault();
                ev.stopPropagation();
                return false;
            })
            .on("awesomplete-select", function(ev) {
                let origin = $(ev.originalEvent.origin);
                console.log('In awesomplete-select')
                console.log(origin)
                let originTagName = origin[0].tagName;
                console.log('originTagName: ' + originTagName);
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
                let data_item_id = origin[0].getAttribute("data-item-id");
                let data_type = origin[0].getAttribute("data-type");
                let data_full_name = origin[0].getAttribute("data-full-name");

                // Emit an event so that the parent vue component can subscribe to the event: 'person-selected' 
                // and receive the data user selected.
                // 
                // id is an Emailuser.id when data_type is 'individual' or 
                // an Organisation.id when data_type is 'organisation'
                vm.$nextTick(() => {
                    let data_item_id_int = parseInt(data_item_id);
                    vm.entity = {
                        'id': data_item_id_int, 
                        'data_type': data_type,
                        'full_name': data_full_name
                    };
                });
            });
        },
        search_person_or_organisation(searchTerm){
            var vm = this;
            let suggest_list_offender = [];
            suggest_list_offender.length = 0;
            vm.awesomplete_obj.list = [];

            /* Cancel all the previous requests */
            if (vm.ajax_for_offender != null) {
                vm.ajax_for_offender.abort();
                vm.ajax_for_offender = null;
            }

            let search_url = "";
            if (vm.searchType == "individual") {
                search_url = "/api/search_user/?search=";
            } else {
                search_url = "/api/search_organisation/?search=";
            }

            vm.ajax_for_offender = $.ajax({
                type: "GET",
                url: search_url + searchTerm + '&exclude_staff=' + vm.excludeStaff + '&departmental_staff=' + vm.departmentalStaff,
                success: function(data) {
                    if (data && data.results) {
                        let persons = data.results;
                        let limit = Math.min(vm.maxItems, persons.length);
                        for (var i = 0; i < limit; i++) {
                        suggest_list_offender.push(persons[i]);
                        }
                    }
                    vm.awesomplete_obj.list = suggest_list_offender;
                    vm.awesomplete_obj.evaluate();
                    // show 'Create' buttons
                    if (searchTerm.length >=2 && suggest_list_offender.length > 0) {
                        if (vm.showCreateUpdate && vm.searchType === 'individual') {
                            vm.showCreateNewPerson = true;
                        } else if (vm.showCreateUpdate && vm.searchType === 'organisation') {
                            vm.showCreateNewOrganisation = true;
                        }
                    }
                },
                error: function(e) {}
            });
        },
    },
    created: async function() {
        this.uuid += 1;
        this.searchType = this.initialSearchType;
        this.$nextTick(()=>{
            if (this.parentEntity) {
                Object.assign(this.entity, this.parentEntity)
            }
            this.initAwesomplete();
        });
        if (this.entityEdit) {
            Object.assign(this.entity, this.entityEdit);
        }
        this.object_hash = hash(this.entity);
        /*
        if (this.departmentalStaff) {
            let returned_departmental_staff = await cache_helper.getSetCacheList(
              'DepartmentalStaff',
              //'https://itassets.dbca.wa.gov.au/api/users/fast/?minimal=true'
              api_endpoints.get_department_users
              );
            Object.assign(this.departmentalStaffList, returned_departmental_staff);
            // blank entry allows user to clear selection
            this.departmentalStaffList.splice(0, 0,
              {
                pk: "",
                //artifact_type: "",
                //description: "",
              });
        }
    */
    },
}
</script>

<style>
.awesomplete > ul {
    margin-top: 0 !important;
    z-index: 10000;
}
.awesomplete > ul > li {
    border-bottom: 1px solid lightgray;
    margin: 5px 10px 5px 10px;
}
</style>
