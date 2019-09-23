import {QuestionFields} from './model'
import {QuestionTemplate} from './html'

export class Controller {

    fields: any
    template: any

    constructor(QuestionFields, QuestionTemplate) {
        this.fields = QuestionFields
        this.template = QuestionTemplate
        this.getFields = this.getFields.bind(this)
        this.getTemplate = this.getTemplate.bind(this)
    }

    getFields() {
        return this.fields
    }

    getTemplate() {
        return this.template
    }

}

export let controller = new Controller(QuestionFields, QuestionTemplate)