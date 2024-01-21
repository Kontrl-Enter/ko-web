var navcontainer = `<div class="flex h-10 flex-row items-center justify-between px-3.5 md:mx-auto md:max-w-[1280px] half-hd:justify-start half-hd:px-0">
            <div class="flex items-center gap-3">
                <a class="flex h-full w-[131px] flex-none items-center" href="/"><svg fill="none" viewBox="0 0 262 40" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" class="h-5 text-white">
                    <svg fill="none" viewBox="0 0 262 40" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" class="h-5 text-white">
                        <img class="h-9 w-15"src="/static/image/logo.png">
                    </svg>
                </a>
                <i class="hidden h-4.5 w-[1px] bg-white opacity-20 desktop:inline-block"></i>
            </div>
        <button class="half-hd:hidden s-3TpKf_vqqt89" type="button">
            <svg fill="none" viewBox="0 0 24 24" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" class="text-white">
                <path fill="currentColor" d="M4.16278 18.525C3.79612 18.525 3.48345 18.4 3.22478 18.15C2.96678 17.9 2.83778 17.5833 2.83778 17.2C2.83778 16.8333 2.96678 16.5207 3.22478 16.262C3.48345 16.004 3.79612 15.875 4.16278 15.875H20.1628C20.5295 15.875 20.8421 16.004 21.1008 16.262C21.3588 16.5207 21.4878 16.8333 21.4878 17.2C21.4878 17.5833 21.3588 17.9 21.1008 18.15C20.8421 18.4 20.5295 18.525 20.1628 18.525H4.16278ZM4.16278 13.325C3.79612 13.325 3.48345 13.196 3.22478 12.938C2.96678 12.6793 2.83778 12.3667 2.83778 12C2.83778 11.6333 2.96678 11.3207 3.22478 11.062C3.48345 10.804 3.79612 10.675 4.16278 10.675H20.1628C20.5295 10.675 20.8421 10.804 21.1008 11.062C21.3588 11.3207 21.4878 11.6333 21.4878 12C21.4878 12.3667 21.3588 12.6793 21.1008 12.938C20.8421 13.196 20.5295 13.325 20.1628 13.325H4.16278ZM4.16278 8.12501C3.79612 8.12501 3.48345 7.99567 3.22478 7.73701C2.96678 7.47901 2.83778 7.16667 2.83778 6.80001C2.83778 6.41667 2.96678 6.10001 3.22478 5.85001C3.48345 5.60001 3.79612 5.47501 4.16278 5.47501H20.1628C20.5295 5.47501 20.8421 5.60001 21.1008 5.85001C21.3588 6.10001 21.4878 6.41667 21.4878 6.80001C21.4878 7.16667 21.3588 7.47901 21.1008 7.73701C20.8421 7.99567 20.5295 8.12501 20.1628 8.12501H4.16278Z">
                </path>
            </svg>
        </button>
        <div class="mr-auto hidden gap-2 pl-6 half-hd:flex half-hd:gap-4 xl:gap-4">
            <div class="relative flex-none">
                <a class="h-10 flex-none justify-center rounded px-2 py-2 text-md font-regular text-white hover:bg-psbl-dark hover:font-medium dark:text-dark-psbk" data-sveltekit-preload-data="tap" href="/statistics">챔피언 숙련도</a> 
            </div> 
            <div class="relative flex-none">
                <a class="h-10 flex-none justify-center rounded px-2 py-2 text-md font-regular text-white hover:bg-psbl-dark hover:font-medium dark:text-dark-psbk" data-sveltekit-preload-data="tap" href="/ranking?lane=-1&amp;page=1&amp;region=kr">개발자 블로그</a> 
            </div> 
            <div class="relative flex-none">
                <a class="h-10 flex-none justify-center rounded px-2 py-2 text-md font-regular text-white hover:bg-psbl-dark hover:font-medium dark:text-dark-psbk" data-sveltekit-preload-data="tap" href="/lab">개발자 연구실</a>
            </div>
        </div>`

const menucontainer = document.getElementById("menu-container");
menucontainer.innerHTML += navcontainer;

