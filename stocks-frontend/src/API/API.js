import axios from "axios";

const ApiURL = process.env.REACT_APP_API_URL
console.log(ApiURL)

const API = axios.create({
    baseURL: ApiURL
})

const fetcher = (url) => API.get(url).then((res) => {
    const paginationHeader = res.headers['x-pagination'];
    return {
        items:[...res.data],
        pagination: paginationHeader ? JSON.parse(paginationHeader) :null
    }
});

export {API, fetcher}