import {
    COLABORADOR_TYPES as TYPES
} from '../../00_types';
import {
    fetchListGet,
    updateObject,
    fetchObject,
    deleteObject,
    createObject,
    callApiMethodPostParameters,
    uploadArchivo
} from '../../00_general_fuctions'

const current_url_api = 'colaboradores';

export const adicionarPuntoVenta = (id, punto_venta_id, options_action = {}) => {
    return (dispatch) => {
        let params = new URLSearchParams();
        params.append('punto_venta_id', punto_venta_id);
        const options = {...options_action, dispatch_method: dispatch};
        callApiMethodPostParameters(current_url_api, id, 'adicionar_punto_venta', params, options)
    }
};

export const quitarPuntoVenta = (id, punto_venta_id, options_action = {}) => {
    return (dispatch) => {
        let params = new URLSearchParams();
        params.append('punto_venta_id', punto_venta_id);
        const options = {...options_action, dispatch_method: dispatch};
        callApiMethodPostParameters(current_url_api, id, 'quitar_punto_venta', params, options)
    }
};

export const createColaborador = (values, options_action = {}) => {
    return (dispatch) => {
        const dispatches = (response) => {
            dispatch({type: TYPES.create, payload: response})
        };
        const options = {dispatches, ...options_action, dispatch_method: dispatch};
        createObject(current_url_api, values, options);
    }
};
export const deleteColaborador = (id, options_action = {}) => {
    return (dispatch) => {
        const dispatches = (response) => {
            dispatch({type: TYPES.delete, payload: id})
        };
        const options = {dispatches, ...options_action, dispatch_method: dispatch};
        deleteObject(current_url_api, id, options);
    }
};
export const fetchColaboradores = (options_action = {}) => {
    return (dispatch) => {
        const dispatches = (response) => {
            dispatch({type: TYPES.fetch_all, payload: response})
        };
        const {limpiar_coleccion = true} = options_action;
        const options = {
            dispatches,
            ...options_action,
            dispatch_method: dispatch,
            clear_action_type: limpiar_coleccion ? TYPES.clear : null
        };
        fetchListGet(current_url_api, options);
    }
};

export const fetchColaborador = (id, options_action = {}) => {
    return (dispatch) => {
        const dispatches = (response) => {
            dispatch({type: TYPES.fetch, payload: response})
        };
        const options = {dispatches, ...options_action, dispatch_method: dispatch};
        fetchObject(current_url_api, id, options);
    }
};
export const clearColaboradores = () => {
    return (dispatch) => {
        dispatch({type: TYPES.clear});

    }
};
export const updateColaborador = (id, values, options_action = {}) => {
    return (dispatch) => {
        const dispatches = (response) => {
            dispatch({type: TYPES.update, payload: response})
        };
        const options = {dispatches, ...options_action, dispatch_method: dispatch};
        updateObject(current_url_api, id, values, options);
    }
};

export const uploadColaboradorFoto = (id, values, options_action = {}) => {
    return (dispatch) => {
        const options = {...options_action, dispatch_method: dispatch};
        uploadArchivo(current_url_api, id, 'upload_archivo', values, options)
    }
};