const $ = require('jquery');
const assetman = require('@pytsite/assetman');

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

export {url, request, get, post, put, patch, del}
