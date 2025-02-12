import axios from "axios";
import qs from "qs"; // 导入 qs 模块

const service = axios.create({
    baseURL: "/api"
})
service.interceptors.request.use((config) => {
    //在发送请求之前做某件事
    if (config.method === 'post' || config.method === 'put') {
        config.data = qs.stringify(config.data);
    }
    return config;
}, (error) => {
    _.toast("错误的传参", 'fail');
    return Promise.reject(error);
});
export default service
