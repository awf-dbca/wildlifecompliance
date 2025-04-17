<template lang="html">
    <div class="container">
        <div class="row panel panel-default confirmation-box">
            <div class="col-md-12">
                <h3>Your Remediation Action has been submitted successfully.</h3>
                <div class="row">
                    <div class="col-md-2" >
                        Reference number:
                    </div>
                    <div class="col-md-4" >
                        {{ remediation_action.remediation_action_id }}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-2" >
                        Lodgement date:
                    </div>
                    <div class="col-md-4" >
                        {{ lodgement_date }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Vue from "vue";
import FormSection from "@/components/forms/section_toggle.vue";
import { api_endpoints, helpers, cache_helper } from "@/utils/hooks";
import { mapState, mapGetters, mapActions, mapMutations } from "vuex";
import filefield from '@/components/common/compliance_file.vue';
//import 'bootstrap/dist/css/bootstrap.css';

export default {
    name: 'RemediationActionSubmitSuccess',
    data() {
        return {
            lodgement_date: null
        }
    },
    components: {

    },
    created: async function() {
        try {
            if (this.$route.params.user_action) {
                this.lodgement_date = this.$route.params.user_action.when;
            }
        } catch (err) {
            this.processError(err);
        }
    },
    mounted: function() {

    },
    computed: {
        ...mapGetters('remediationActionStore', {
            remediation_action: "remediation_action",
        }),
    },
    methods: {
        processError: async function(err){
            let errorText = '';
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
                        errorText += field_name + ':<br />';
                        for (let j=0; j<err.body[field_name].length; j++){
                            errorText += err.body[field_name][j] + '<br />';
                        }
                    }
                }
            }
            await swal("Error", errorText, "error");
        },
    }
}
</script>

<style>
.button-gap {
    margin: 0 0 0 1em;
}
.confirmation-box {
    padding: 0 0 1.5em 0;
}

</style>
