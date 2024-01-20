var footcontainer=`<div class="mx-auto flex w-full flex-col gap-8 px-4 pb-14 pt-6 desktop:w-[1100px] desktop:gap-12 desktop:pb-24">
            <div class="flex flex-col items-center w-full gap-8 px-0 mobile-small:px-4 mobile-large:px-10 desktop:flex-row desktop:items-center desktop:justify-between desktop:px-0">
                <ul class="flex flex-wrap justify-center gap-6 font-medium gap-y-1 text-rg">
                    <li class="inline-flex h-6">
                        <a class="py-1 whitespace-nowrap hover:text-primary-medium dark:hover:text-primary-bright" href="https://developer.riotgames.com/docs/lol">관련문서</a>
                    </li> 
                    <li class="inline-flex h-6">
                        <a class="py-1 whitespace-nowrap hover:text-primary-medium dark:hover:text-primary-bright" href="https://developer.riotgames.com/policies/general">이용약관</a>
                    </li>
                    <li class="inline-flex h-6">
                        <a class="py-1 whitespace-nowrap hover:text-primary-medium dark:hover:text-primary-bright" >버그리포팅(개발예정)</a>
                    </li>
                </ul> 
                <ul class="flex flex-col items-center justify-center gap-2 desktop:flex-row desktop:gap-6">
                    <li class="text-center">
                        <a href="https://www.riotgames.com/kr" target="_blank" rel="noopener noreferrer" class="flex items-center text-rg font-bold text-[#5865F2] opacity-80 hover:opacity-100">
                            <div class="h-7 w-7 px-1 py-1 text-[#5865F2]">
                                <image src="https://yt3.googleusercontent.com/ytc/AIf8zZQskdbpL9wlq1y-N5sHZY1L__ap1g-e6rxFJYmoPQ=s900-c-k-c0x00ffffff-no-rj"></image>
                            </div>
                            <p class="font-bold"style="color: red;">RIOT GAMES</p>
                        </a>
                    </li> 
                    <li class="text-center">
                        <a href="https://www.riotgames.com/kr" target="_blank" rel="noopener noreferrer" class="opacity-80 hover:opacity-100">
                        </a>
                    </li>
                    <li class="text-center">
                        <a href="https://developer.riotgames.com/" target="_blank" rel="noopener noreferrer" class="flex items-center text-rg font-bold gap-1 text-[#5865F2] opacity-80 hover:opacity-100">
                            <div class="h-8 w-8 px-1 py-1 text-[#5865F2]">
                                <image src="data:image/png;base64,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"></image>
                            </div>
                            <p class="font-bold"style="color: black;">Riot Developer Portal</p>
                        </a>
                    </li> 
                    <li class="text-center">
                        <a href="https://developer.riotgames.com/" target="_blank" rel="noopener noreferrer" class="opacity-80 hover:opacity-100">
                        </a>
                    </li>
                </ul>
            </div> 
            <div class="flex w-full flex-col gap-2 self-center desktop:max-w-[800px]">
                <p class="text-center text-[10px] font-light leading-[16px]">This site isn’t endorsed by Riot Games and doesn’t reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. This site was created based on Api data recieved from Riot Developer Portal, Riot Games. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.</p> 
                <p class="text-sm font-medium text-center">producer Kogeonu</p>
            </div>
        </div>`

const footercontainer = document.getElementById("footer-container");
footercontainer.innerHTML += footcontainer;