import axios from "axios";

const ApiURL = process.env.REACT_APP_API_URL
console.log(ApiURL)

const API = axios.create({
    baseURL: ApiURL
})

const fetcher = (url) => API.get(url).then((res) => {
    return {
        items:[...res.data],
        pagination: JSON.parse(res.headers['x-pagination'])
    }
});

export {API, fetcher}