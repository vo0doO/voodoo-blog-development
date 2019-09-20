export class QuestionFields {

    len: number
    
    field:  {
        
        count:number
        name: string
        lable: string
        id: number
        checked: boolean
        visible: boolean

        choices: {

            len: number
            
            choice:{
                count: number
                name: string
                lable: string
                input_type
                id: number
                checked: boolean
            }
        }
    }

    constructor () {

    }
}