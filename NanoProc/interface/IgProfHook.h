#ifndef CMGTools_NanoProc_IgProfHook_h
#define CMGTools_NanoProc_IgProfHook_h

bool setupIgProfDumpHook() ;

class SetupIgProfDumpHook {
    public:
        SetupIgProfDumpHook() ;
        ~SetupIgProfDumpHook() ;
        void start() ; 
};

#endif
