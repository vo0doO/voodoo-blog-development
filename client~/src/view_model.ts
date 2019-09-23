import { Controller, controller } from './controller'


export class ViewModel {

    template:any
    fields: any
    current_fields_list: any[]
    rendered_templates_list: any[]

    constructor (QuestionFields, QuestionTemplate) {
        this.template = QuestionTemplate
        this.fields = QuestionFields
        this.renderTemplate = this.renderTemplate.bind(this)
    }

    renderTemplate() {
        for (let field of this.fields) {
            this.current_fields_list.push(field)
            // TODO: create Map for hashing this.field and him choice
            } 
        }
    }
}
