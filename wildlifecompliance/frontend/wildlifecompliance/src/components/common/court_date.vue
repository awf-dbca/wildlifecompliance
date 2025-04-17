<template lang="html">
    <div class="form-group">
        <div class="flexContainer">
            <label class="flexItemTitleDatetime">Court</label>

            <div class="flexItemDatetime" v-if="courts.length > 0">
                <select :disabled="readonlyForm" class="form-control" v-model="court_location" @change="emitEvent()">
                    <option value=""></option>
                    <option v-for="co in courts" :value="co" :key="co.id">
                        {{ co.identifier }}
                    </option>
                </select>
            </div>

            <input type="text" v-if="court_location" :value="court_location.location" class="form-control" disabled />
        </div>

        <div class="flexContainer">
            <label class="flexItemTitleDatetime">Date</label>
            <div class="flexItemDatetime">
                <div class="input-group date" ref="courtDatePicker">
                    <input :readonly="readonlyForm" type="text" class="form-control" :value="court_date" />
                    <span class="input-group-addon">
                        <span class="glyphicon glyphicon-calendar"></span>
                    </span>
                </div>
            </div>

            <label class="flexItemTitleDatetime">Time</label>
            <div class="flexItemDatetime">
                <div class="input-group date" ref="courtTimePicker">
                    <input :readonly="readonlyForm" type="text" class="form-control" :value="court_time" />
                    <span class="input-group-addon">
                        <span class="glyphicon glyphicon-calendar"></span>
                    </span>
                </div>
            </div>

            <label class="flexItemTitleComments">Comments</label>
            <div class="flexItemComments">
                <input :readonly="readonlyForm" type="text" class="form-control" v-model="court_comments" ref="courtComments" />
            </div>
        </div>
    <hr>
    </div>
</template>

<script>
import Vue from "vue";
import { api_endpoints, helpers, cache_helper } from "@/utils/hooks";
import utils from "@/components/external/utils";
import { mapState, mapGetters, mapActions, mapMutations } from "vuex";
import moment from 'moment';
import datatable from '@vue-utils/datatable.vue'
//import 'bootstrap/dist/css/bootstrap.css';
//import 'eonasdan-bootstrap-datetimepicker';
import _ from 'lodash';

export default {
    name: "CourtDate",
    data: function() {
        return {
            uuid: 0,
            court_date: null,
            court_time: null,
            court_comments: '',
            court_location: null,
            courts: [],
        }
    },
    components: {

    },
    props:{
        court_datetime: {
            type: Date,
            default: null,
        },
        comments: {
            type: String,
            default: '',
        },
        court: {
            type: Object,
            default: null,
        },
        court_date_id: {
            type: Number,
            default: null,
        },
        return_date_format: {
            type: String,
            default: 'DD/MM/YYYY',
        },
        return_time_format: {
            type: String,
            default: 'HH:mm',
        },
        court_in_future: {
            type: Boolean,
            default: true,
        }
    },
    computed: {
        ...mapGetters('legalCaseStore', {
            legal_case: "legal_case",
        }),
        csrf_token: function() {
            return helpers.getCookie("csrftoken");
        },
        readonlyForm: function() {
            let readonly = true
            if (this.legal_case && this.legal_case.id && !this.closedStatus && this.court_in_future) {
                readonly = !this.legal_case.can_user_action;
            }
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
    },
    methods: {
        ...mapActions('legalCaseStore', {

        }),
        courtOutcomeDocumentUploaded: function() {
            console.log('courtOutcomeDocumentUploaded');
        },
        emitEvent: function() {
            // Construct moment to emit
            let test_m_datetime = moment(this.court_date + ' ' + this.court_time, 'DD/MM/YYYY LT');
            this.$emit('data_changed', {
                id: this.court_date_id,
                court_datetime: test_m_datetime,
                comments: this.court_comments,
                court: this.court_location,
            });
        },
        addEventListeners: function() {
            let vm = this;
            let el_court_date = $(vm.$refs.courtDatePicker);
            let el_court_time = $(vm.$refs.courtTimePicker);

            // Date
            el_court_date.datetimepicker({
                format: "DD/MM/YYYY",
                showClear: true,
                date: vm.court_datetime,
            });
            el_court_date.on("dp.change", function(e) {
                if (el_court_date.data("DateTimePicker").date()) {
                    vm.court_date = e.date.format('DD/MM/YYYY');
                } else if (el_court_date.data("date") === "") {
                    vm.court_date = null;
                }
                vm.emitEvent();
            });

            // Time
            el_court_time.datetimepicker({
                format: "LT", 
                showClear: true,
                date: vm.court_datetime,
            });
            el_court_time.on("dp.change", function(e) {
                if (el_court_time.data("DateTimePicker").date()) {
                    vm.court_time = e.date.format('LT');
                } else if (el_court_time.data("date") === "") {
                    vm.court_time = null;
                }
                vm.emitEvent();
            });

            // Comments
            let el_comments = $(vm.$refs.courtComments);
            el_comments.on('keyup', function(e){
                try {
                    vm.emitEvent();
                } catch (err) {
                    console.log(err); 
                }
            });
        },
        constructOptionsCourt: async function() {
            let returned= await cache_helper.getSetCacheList('CourtProceedings_Courts', '/api/legal_case/court_list');
            this.courts = returned;
        },
    },
    created: async function() {
        this.constructOptionsCourt();
    },
    mounted: function() {
        console.log('mounted');
        this.$nextTick(() => {
            this.addEventListeners();
        });
        // Convert datetime representation in string to moment obj
        console.log(this.court_datetime);
        if (this.court_datetime){
            let court_datetime_obj = moment(new Date(this.court_datetime.getTime()));
            // Assign date as String type
            this.court_date = court_datetime_obj.format('DD/MM/YYYY');
            // Assign time as String type
            this.court_time = court_datetime_obj.format('LT');
        }
        this.court_comments = this.comments;
        this.court_location = this.court;
    },
};
</script>

<style lang="css">
.bottom-align-text {

}
.flexContainer {
    display: flex;
    align-items: center;
    margin: 0 0 1em 0;
}
.flexItemTitleDatetime {
    width: 5%;
    margin-right: 1em;
}
.flexItemTitleComments {
    width: 14%;
    text-align: right;
    margin-right: 1em;
}
.flexItemDatetime {
    width: 20%;
    margin: 0 3% 0 0;
}
.flexItemComments {
    width: 40%;
}
</style>
