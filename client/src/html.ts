export let QuestionTemplate:string = 

    `<main 
        id="${this.field.name}" 
        role="main" 
        class="lead"
        >
        <p class="lead">

            <label>
                <h1 
                    class="cover-heading"
                    >${this.field.lable}
                </h1>
            </label>

            <br/>

            <table 
                align="center" 
                class="lead" 
                id="id_${this.field.name}"
                >
                    <tr 
                        align="center" 
                        class="lead"
                        >
                        <td 
                            class="lead">
                            <label 
                                class="lead" 
                                for="id_${this.field.name}_${this.field.choice.count}">
                                <input type="${this.field.choice.input_type}" 
                                    name="${this.field.name}" 
                                    value="${this.field.choice.name}" 
                                    id="id_${this.field.name}_${this.field.choice.count}"
                                    >${this.field.choice.lable}
                            </label>
                        </td>
                    </tr>
            <button 
                id="${this.field.name}-btn"
                type="${"submit" ? "#" : this.field.count === this.fields.length()}"
                disabled="${this.field.checked}" 
                class="btn btn-lg btn-secondary"
                >${"Дальше" ? "Сохранить" : this.field.count === this.fields.length()}
            </button>
        </p>
    </main>`
