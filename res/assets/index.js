import $ from 'jquery';

const currentLang = document.documentElement.getAttribute('lang');

function request(method, endpoint, data = {}) {
    return new Promise((resolve, reject) => {
        if (!endpoint.startsWith('http'))
            endpoint = new URL(`api/${endpoint}`, window.location.origin);

        const ajaxSettings = {
            url: endpoint,
            method: method,
            data: data,
            headers: {'Accept-Language': currentLang}
        };

        if (data instanceof FormData) {
            ajaxSettings.processData = false;
            ajaxSettings.contentType = false;
        }

        $.ajax(ajaxSettings).done(data => resolve(data)).fail(jqXHR => reject(jqXHR));
    });
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
    request: request,
    get: get,
    post: post,
    put: put,
    patch: patch,
    del: del
};

export default api;
