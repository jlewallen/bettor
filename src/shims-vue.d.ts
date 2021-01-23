declare module "*.vue" {
    import Vue from "vue";

    export default Vue;
}

// https://github.com/vuematerial/vue-material/issues/662
declare module "vue-material" {
    import _Vue from "vue";

    export default any;

    // export default type PluginFunction<T> = (Vue: typeof _Vue, options?: T) => void;
    // export function MdButton(Vue: typeof _Vue, options?: any): void;
    // export function MdContent(Vue: typeof _Vue, options?: any): void;
    // export function MdTabs(Vue: typeof _Vue, options?: any): void;
    // export function MdForms(Vue: typeof _Vue, options?: any): void;
}
