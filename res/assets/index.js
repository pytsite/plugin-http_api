import $ from 'jquery';
import assetman from '@pytsite/assetman';

function url(endpoint, data = {}) {
    if (!endpoint.startsWith('http'))
        endpoint = '/api/' + endpoint;

    return assetman.url(endpoint, data)
}

function request(method, endpoint, data = {}) {
    let ajaxSettings = {
        url: url(endpoint),
        method: method,
        data: data,
        headers: {'Accept-Language': document.documentElement.getAttribute('lang')}
    };

    if (data instanceof FormData) {
        ajaxSettings.processData = false;
        ajaxSettings.contentType = false;
    }

    return $.ajax(ajaxSettings);
}

function get(endpoint, data) {
    return request('GET', endpoint, data)
}

function post(endpoint, data) {
    return request('POST', endpoint, data)
}

function put(endpoint, data) {
    return request('PUT', endpoint, data)
}

function patch(endpoint, data) {
    return request('PATCH', endpoint, data)
}

function del(endpoint, data) {
    return request('DELETE', endpoint, data)
}

const api = {
    url: url,
    request: request,
    get: get,
    post: post,
    put: put,
    patch: patch,
    del: del
};

export default api;