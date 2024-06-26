import Vue from 'vue';
import {
    api_endpoints,
    helpers
}
from '@/utils/hooks';
import moment from 'moment';

export const callemailStore = {
    namespaced: true,
    state: {
        call_email: {
            schema: [],
            classification: {
                id: null,
            },
            location: {
                type: "Feature",
                properties: {
                    town_suburb: null,
                    street: null,
                    state: 'WA',
                    postcode: null,
                    country: 'Australia',
                    details: ''
                },
                geometry: {
                    "type": "Point",
                    "coordinates": [],
                },
            },
            call_type: {
                id: null,
            },
            report_type: {
                id: null,
            },
            //allocated_group: {
              //  members: [],
            //},
            allocated_group: [],
            volunteer_list: [],
        },
        classification_types: [],
        call_types: [],
        report_types: [],
        referrers: [],
        status_choices: [],
    },
    getters: {
        call_email: state => state.call_email,
        classification_types: state => state.classification_types,
        report_types: state => state.report_types,
        status_choices: state => state.status_choices,
        referrers: state => state.referrers,
        call_latitude(state) {
            if (state.call_email.location) {
                if (state.call_email.location.geometry) {
                    if (state.call_email.location.geometry.coordinates.length > 0) {
                        return state.call_email.location.geometry.coordinates[1];
                    } else {return "";}
                } else {return "";}
            } else {return "";}
        },
        call_longitude(state) {
            if (state.call_email.location) {
                if (state.call_email.location.geometry) {
                    if (state.call_email.location.geometry.coordinates.length > 0) {
                        return state.call_email.location.geometry.coordinates[0];
                    } else {return "";}
                } else {return "";}
            } else {return "";}
        },
    },
    mutations: {
        updateStatusChoices(state, choices) {
            for (var i = 0; i < choices.length; i++) {
                state.status_choices.push(choices[i]);
            }
        },
        updateClassificationChoices(state, choices) {
            for (var i = 0; i < choices.length; i++) {
                state.classification_types.push(choices[i]);
            }
        },
        updateCallEmail(state, call_email) {
            if (!call_email.location) {
                /* When location is null, set default object */
                call_email.location =
                {
                    "type": "Feature",
                    properties: {
                        town_suburb: null,
                        street: null,
                        state: null,
                        postcode: null,
                        country: null,
                    },
                    id: null,
                    geometry: {
                        "type": "Point",
                        "coordinates": [],
                    },
                };
            }
            if (!call_email.email_user){
                /* When email_user is null, set default object */
                call_email.email_user = {
                    first_name: '',
                    last_name: '',
                    dob: null,
                    residential_address: {
                        line1: '',
                        locality: '',
                        state: 'WA',
                        postcode: '',
                        country: 'AU'
                    }
                };
            } else if (!call_email.email_user.residential_address){
                /* When residential_address is null, set default object */
                call_email.email_user.residential_address = {
                    line1: '',
                    locality: '',
                    state: 'WA',
                    postcode: '',
                    country: 'AU'
                };
            }
            Vue.set(state, 'call_email', {
                ...call_email
            });
            if (state.call_email.occurrence_date_from) {
                state.call_email.occurrence_date_from = moment(state.call_email.occurrence_date_from, 'YYYY-MM-DD').format('DD/MM/YYYY');
            }
            if (state.call_email.occurrence_time_start) {
                state.call_email.occurrence_time_start = moment(state.call_email.occurrence_time_start, 'HH:mm').format('hh:mm A');
            } else if (state.call_email.occurrence_time_start === '') {
                state.call_email.occurrence_time_start = null;
            }
            if (state.call_email.occurrence_date_to) {
                state.call_email.occurrence_date_to = moment(state.call_email.occurrence_date_to, 'YYYY-MM-DD').format('DD/MM/YYYY');
            }
            if (state.call_email.occurrence_time_end) {
                state.call_email.occurrence_time_end = moment(state.call_email.occurrence_time_end, 'HH:mm').format('hh:mm A');
            } else if (state.call_email.occurrence_time_end === '') {
                state.call_email.occurrence_time_end = null;
            }
            if (state.call_email.date_of_call) {
                state.call_email.date_of_call = moment(state.call_email.date_of_call, 'YYYY-MM-DD').format('DD/MM/YYYY');
            }
            if (state.call_email.time_of_call) {
                state.call_email.time_of_call = moment(state.call_email.time_of_call, 'HH:mm').format('hh:mm A');
            } else if (state.call_email.time_of_call === '') {
                state.call_email.time_of_call = null;
            }
            if (!state.call_email.volunteer_id) {
                state.call_email.volunteer_id = state.call_email.current_user_id;
            }
            let rendererDocumentUrl = helpers.add_endpoint_join(
                api_endpoints.call_email,
                state.call_email.id + "/process_renderer_document/"
                )
            Vue.set(state.call_email, 'rendererDocumentUrl', rendererDocumentUrl); 
            let commsLogsDocumentUrl = helpers.add_endpoint_join(
                api_endpoints.call_email,
                state.call_email.id + "/process_comms_log_document/"
                )
            Vue.set(state.call_email, 'commsLogsDocumentUrl', commsLogsDocumentUrl); 
        },
        updateSchema(state, schema) {
            //state.call_email.schema = schema;
            Vue.set(state.call_email, 'schema', schema);
        },        
        updateClassificationTypes(state, classification_entry) {
            if (classification_entry) {
                state.classification_types.push(classification_entry);
            } else {
                state.classification_types = [];
            }
        },
        updateReferrers(state, referrer_entry) {
            if (referrer_entry) {
                state.referrers.push(referrer_entry);
            } else {
                state.referrers = [];
            }
        },
        updateReportTypes(state, report_type_entry) {
            if (report_type_entry) {
                state.report_types.push(report_type_entry);
            } else {
                state.report_types = [];
            }
        },
        updateClassification(state, classification) {
            if (classification) {
                Vue.set(state.call_email, 'classification', classification);
            }
        },
        updateReportType(state, report_type) {
            if (report_type) {
                Vue.set(state.call_email, 'report_type', report_type);
            }
        },
        updateEmailUser(state, email_user){
            if (email_user){
                Vue.set(state.call_email, 'email_user', email_user);
            }
        },
        updateEmailUserEmpty(state){
            let email_user_empty = {
                first_name: '',
                last_name: '',
                dob: null,
                residential_address: {
                    line1: '',
                    locality: '',
                    state: 'WA',
                    postcode: '',
                    country: 'AU'
                }
            };
            Vue.set(state.call_email, 'email_user', email_user_empty);
        },
        updateResidentialAddress(state, address){
            Vue.set(state.call_email.email_user, 'residential_address', address);
        },
        updateLocation(state, location) {
            Vue.set(state.call_email, 'location', location);
        },
        updateLocationPoint(state, point) {
            state.call_email.location.geometry.coordinates = point;
        },
        updateLocationAddress(state, location_properties) {
            state.call_email.location.properties = location_properties;
        },
        updateLocationAddressEmpty(state) {
            state.call_email.location.properties.town_suburb = "";
            state.call_email.location.properties.street = "";
            state.call_email.location.properties.state = "";
            state.call_email.location.properties.postcode = "";
            state.call_email.location.properties.country = "";
        },
        updateLocationDetailsFieldEmpty(state) {
            state.call_email.location.properties.details = "";
        },
        updateAllocatedGroupList(state, members) {
            Vue.set(state.call_email, 'allocated_group', {});
            Vue.set(state.call_email, 'allocated_group', members);
        },
        updateAllocatedGroupId(state, id) {
            state.call_email.allocated_group_id = id;
        },
        updateRegionId(state, id) {
            state.call_email.region_id = id;
        },
        updateOccurrenceTimeStart(state, time) {
            Vue.set(state.call_email, 'occurrence_time_start', time);
        },
        updateOccurrenceTimeEnd(state, time) {
            Vue.set(state.call_email, 'occurrence_time_end', time);
        },
        updateTimeOfCall(state, time) {
            Vue.set(state.call_email, 'time_of_call', time);
        },
        updateDateOfCall(state, date) {
            Vue.set(state.call_email, 'date_of_call', date);
        },
        updateRelatedItems(state, related_items) {
            Vue.set(state.call_email, 'related_items', related_items);
        },
        updateCaller(state, data) {
            if (data.data_type === 'individual') {
                Vue.set(state.call_email, 'email_user_id', data.id);
            }
        },
    },
    actions: {
        async loadCallEmail({ dispatch, commit }, { call_email_id }) {
            try {
                const returnedCallEmail = await Vue.http.get(
                    helpers.add_endpoint_json(
                        api_endpoints.call_email, 
                        call_email_id)
                    );

                /* Set CallEmail object */
                await dispatch("setCallEmail", returnedCallEmail.body);

                for (let form_data_record of returnedCallEmail.body.data) {
                    await dispatch("setFormValue", {
                        key: form_data_record.field_name,
                        value: {
                            "value": form_data_record.value,
                            "comment_value": form_data_record.comment,
                            "deficiency_value": form_data_record.deficiency,
                        }
                    }, {
                        root: true
                    });
                }

            } catch (err) {
                //console.log(err);
            }
        },
        async saveCallEmailPerson({dispatch, state}){
            try{
                let fetchUrl = helpers.add_endpoint_join(api_endpoints.call_email, state.call_email.id + "/call_email_save_person/");
                const savedEmailUser = await Vue.http.post(fetchUrl, state.call_email);
                await dispatch("setEmailUser", savedEmailUser.body);
                await swal("Saved", "The record has been saved", "success");
            } catch (err) {
                //console.log(err);
                if (err.body.non_field_errors){
                    await swal("Error", err.body.non_field_errors[0], "error");
                } else {
                    await swal("Error", "There was an error saving the record", "error");
                }
            }
        },
        //async saveCallEmail({ dispatch, state, rootGetters}, { crud, internal, close }) {
        async saveCallEmail({ dispatch, state, rootGetters}, { crud, internal }) {
            let callId = null;
            let savedCallEmail = null;
            try {

                let payload = new Object();
                Object.assign(payload, state.call_email);
                if (payload.occurrence_date_from) {
                    payload.occurrence_date_from = moment(payload.occurrence_date_from, 'DD/MM/YYYY').format('YYYY-MM-DD');
                } else if (payload.occurrence_date_from === '') {
                    payload.occurrence_date_from = null;
                }
                if (payload.occurrence_time_start) {
                    payload.occurrence_time_start = moment(payload.occurrence_time_start, 'hh:mm A').format('HH:mm');
                } else if (payload.occurrence_time_start === '') {
                    payload.occurrence_time_start = null;
                }
                if (payload.occurrence_date_to) {
                    payload.occurrence_date_to = moment(payload.occurrence_date_to, 'DD/MM/YYYY').format('YYYY-MM-DD');
                } else if (payload.occurrence_date_to === '') {
                    payload.occurrence_date_to = null;
                }
                if (payload.occurrence_time_end) {
                    payload.occurrence_time_end = moment(payload.occurrence_time_end, 'hh:mm A').format('HH:mm');
                } else if (payload.occurrence_time_end === '') {
                    payload.occurrence_time_end = null;
                }
                if (payload.date_of_call) {
                    payload.date_of_call = moment(payload.date_of_call, 'DD/MM/YYYY').format('YYYY-MM-DD');
                } else if (payload.date_of_call === '') {
                    payload.date_of_call = null;
                }
                if (payload.time_of_call) {
                    payload.time_of_call = moment(payload.time_of_call, 'hh:mm A').format('HH:mm');
                } else if (payload.time_of_call === '') {
                    payload.time_of_call = null;
                }
                if (crud == 'duplicate') {
                    payload.id = null;
                    payload.location_id = null;
                    if (payload.location) {
                        payload.location.id = null;
                    }
                }

                if (state.call_email.schema) {
                if (state.call_email.schema.length > 0) {
                    payload.renderer_data = rootGetters.renderer_form_data;
                    }
                }

                if (crud === 'create') {
                    const createUrl = api_endpoints.call_email;
                    savedCallEmail = await Vue.http.post(createUrl, {});
                } else if (crud === 'duplicate') {
                    const createUrl = api_endpoints.call_email;
                    savedCallEmail = await Vue.http.post(createUrl, payload);
                } else if (crud === 'save') {
                        //---Save the draft call/email
                        const draftUrl = helpers.add_endpoint_join(
                        api_endpoints.call_email,
                        state.call_email.id + "/draft/")
                    try {
                        savedCallEmail = await Vue.http.post(draftUrl, payload)
                    }catch(err) {
                        await swal({
                            title: 'Error',
                            html: helpers.formatError(err),
                            type: "error",
                        })
                    }
                } else {
                    try {
                        const fetchUrl = helpers.add_endpoint_join(
                        api_endpoints.call_email, 
                        state.call_email.id + "/"
                        )
                        savedCallEmail = await Vue.http.put(fetchUrl, payload)
                    }catch(err) {
                        await swal({
                            title: 'Mandatory Field',
                            html: helpers.formatError(err),
                            type: "error",
                        })
                    }
                }

                await dispatch("setCallEmail", savedCallEmail.body);
                callId = savedCallEmail.body.id;

            } catch (err) {
                //console.log(err);
                if (internal) {
                    // return "There was an error saving the record";
                    return err;
                } else {
                    await swal("Error", "There was an error saving the record", "error");
                }
                //return window.location.href = "/internal/call_email/";
            }
            if (crud === 'duplicate') {
                console.log("hello???")
                return window.location.href = "/internal/call_email/" + callId;
            }
            else if (crud !== 'create') {
                if (!internal) {
                    await swal("Saved", "The record has been saved", "success");
                } else {
                    return savedCallEmail;
                }
            }
            return savedCallEmail;
        },
        setAllocatedGroupList({ commit }, data) {
            commit('updateAllocatedGroupList', data);
        },
        setRegionId({ commit }, id) {
            commit('updateRegionId', id);
        },
        setAllocatedGroupId({ commit, }, id) {
            commit("updateAllocatedGroupId", id);
        },
        setCallID({ commit, }, id) {
            commit("updateCallID", id);
        },
        setSchema({ commit, }, schema) {
            commit("updateSchema", schema);
        },
        setEmailUser({ commit, }, email_user) {
            commit("updateEmailUser", email_user);
        },
        setEmailUserEmpty({ commit, }){
            commit("updateEmailUserEmpty");
        },
        setResidentialAddress({ commit }, address){
            commit("updateResidentialAddress", address);
        },
        setLocation({ commit, }, location) {
            commit("updateLocation", location);
        },
        setLocationAddress({ commit, }, location_properties) {
            commit("updateLocationAddress", location_properties);
        },
        setLocationAddressEmpty({ commit, }) {
            commit("updateLocationAddressEmpty");
        },
        setLocationDetailsFieldEmpty({ commit, }) {
            commit("updateLocationDetailsFieldEmpty");
        },
        setLocationPoint({ commit, }, point) {
            commit("updateLocationPoint", point);
        },
        setClassificationEntry({ commit, }, classification_entry) {
            commit("updateClassificationTypes", classification_entry);
        },
        setReferrerEntry({ commit, }, referrer_entry) {
            commit("updateReferrers", referrer_entry);
        },
        setReportTypeEntry({ commit, }, report_type_entry) {
            commit("updateReportTypes", report_type_entry);
        },
        setCallEmail({ commit, }, call_email) {
            commit("updateCallEmail", call_email);
        },
        setReportType({ commit, }, report_type) {
            commit("updateReportType", report_type)
        },
        setClassification({ commit, }, classification) {
            commit("updateClassification", classification)
        },
        setOccurrenceTimeStart({ commit }, time ) {
            commit("updateOccurrenceTimeStart", time);
        },
        setOccurrenceTimeEnd({ commit }, time ) {
            commit("updateOccurrenceTimeEnd", time);
        },
        setTimeOfCall({ commit }, time ) {
            commit("updateTimeOfCall", time);
        },
        setDateOfCall({ commit }, date ) {
            commit("updateDateOfCall", date);
        },
        setRelatedItems({ commit }, related_items ) {
            commit("updateRelatedItems", related_items);
        },
        setCaller({ commit }, data) {
            commit("updateCaller", data);
        },
    },
};
