const { default: axios } = require('axios');

class RegisterService{
    constructor(){
        this.URI = 'http://localhost:5000/register';
    }

    addClient(client){
        console.log(client)
        return axios.post(this.URI, client, {withCredentials: true})
    }
}

export default RegisterService;