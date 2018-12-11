import $ from 'jquery';
import assetman from '@pytsite/assetman';

const currentLang = document.documentElement.getAttribute('lang');

function url(endpoint, args) {
    if (!endpoint.startsWith('http'))
        endpoint = new URL(`api/${endpoint}`, window.location.origin).toString();

    if (args)
        endpoint = assetman.url(endpoint, args);

    return endpoint;
}

async function request(method, endpoint, data = {}, returnResponseObject = false) {
    return new Promise((resolve, reject) => {
        const ajaxSettings = {
            url: url(endpoint),
            method: method,
            data: data,
            headers: {'Accept-Language': currentLang}
        };

        if (data instanceof FormData) {
            ajaxSettings.processData = false;
            ajaxSettings.contentType = false;
        }

        $.ajax(ajaxSettings).done((data, textStatus, response) => {
            returnResponseObject ? resolve({data: data, response: response}) : resolve(data);
        }).fail(response => {
            reject(response)
        });
    });
}

async function get(endpoint, data, returnResponseObject = false) {
    return request('GET', endpoint, data, returnResponseObject)
}

async function post(endpoint, data, returnResponseObject = false) {
    return request('POST', endpoint, data, returnResponseObject)
}

async function put(endpoint, data, returnResponseObject = false) {
    return request('PUT', endpoint, data, returnResponseObject)
}

async function patch(endpoint, data, returnResponseObject = false) {
    return request('PATCH', endpoint, data, returnResponseObject)
}

async function del(endpoint, data, returnResponseObject = false) {
    return request('DELETE', endpoint, data, returnResponseObject)
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
