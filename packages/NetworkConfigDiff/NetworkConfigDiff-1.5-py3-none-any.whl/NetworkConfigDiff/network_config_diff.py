import difflib
import json

class ConfigDiff(object):

    def __init__(self, old_config, new_config):
        self.old_config = old_config
        self.new_config = new_config

    def _get_level(self,data):
        name = data.lstrip(' ')
        level =  len(data) - len(name)
        return level

    def get_true_before(self,text,target_line_number,level,fromdata_data):
        '''
        返回：{'bgp 65139': {}},{'global': {}}
        '''
        config_line = text
        # print(len(config_line))
        line = config_line[target_line_number-1].rstrip('\n')
        # print(line,target_line_number)
        conf_for_nowstrip = line.lstrip(' ')
        curr_level = self._get_level(line)
        # print(conf_for_nowstrip)
        # print(len(line), len(conf_for_nowstrip))
        
        if curr_level < level:
            flag = ''
            if len(line) == len(conf_for_nowstrip):
                result = {}
                # print(conf_for_nowstrip + '123', type(conf_for_nowstrip))
                if conf_for_nowstrip == '#':
                    result[fromdata_data] = {}
                    flag = '#'
                elif conf_for_nowstrip == '!':
                    # if not result.get('global'):
                    #     result['global'] = {}
                    flag = '!'
                    result[fromdata_data] = {}
                else:
                    result[conf_for_nowstrip] = {}
                    result[conf_for_nowstrip][fromdata_data] = {}
                # print('result值{}'.format(result))
                return result,flag
            else:
                # 三层，二层
                result,flag = self.get_true_before(text,target_line_number-1,curr_level,fromdata_data) # 
                # return {conf_for_nowstrip:result}
                key = list(result.keys())[0]
                value = list(result[key].keys())[0]
                # print('key是{},result是{},{},{}'.format(key,result,conf_for_nowstrip,value))
                result[key][line] = {}
                result[key][line][value] = {}
                del result[key][value]
                # print(result)
                return result,flag
        elif curr_level == level:
            for i in range(1, target_line_number):
                target_level = self._get_level(config_line[target_line_number-i])
                # print(config_line[target_line_number-i])
                # print(target_level)
                # print(level)
                if target_level == level:
                    continue
                else:
                    # print(i)
                    return self.get_true_before(text,target_line_number+1-i,level,fromdata_data) # {'bgp 65139': {}}

    def _merge_dicts(self,*dicts):
        """
        合并多个字典，其中每个字典可能包含多个嵌套级别的子字典
        """
        result = {}
        for dictionary in dicts:
            if dictionary:
                for key, value in dictionary.items():
                    if isinstance(value, dict):
                        result[key] = self._merge_dicts(result.get(key, {}), value)
                    else:
                        result[key] = value
        return result

    def collect_lines(self,diffs):
        # 生成数组 {{'global':{'aa':{},'bb':{}}},{'bgp':{'cc':{},'dd':{}}}}
        from_all_info = {}
        to_all_info = {}
        for fromdata,todata,flag in diffs:
            if flag:
                # print(fromdata,todata,flag)
                fromdata_num,fromdata_data = fromdata
                fromdata_data = fromdata_data.replace('\0+', '')
                fromdata_data = fromdata_data.replace('\0-', '')
                fromdata_data = fromdata_data.replace('\0^', '')
                # print(fromdata_data, type(fromdata_data))
                # fromdata_data = move_flag_to_behind(fromdata_data)
                fromdata_data = fromdata_data.replace('\1', '')
                # fromdata_data = fromdata_data.replace('\x00', '')
                # print('1fromdata_data{}'.format(fromdata_data))
                level = self._get_level(fromdata_data)
                # print('level为{}'.format(level))
                if fromdata_data != '\n' and fromdata_num!='':
                    # print('1fromdata_data{}'.format(fromdata_data))
                    if level == 0:
                        # if not from_all_info.get('global'):
                        #     from_all_info['global'] = {}
                        from_all_info[fromdata_data] = {}
                    else:
                        output,self.flag = self.get_true_before(text_b,fromdata_num-1,level, fromdata_data)
                        print(output)
                        from_all_info  = self._merge_dicts(from_all_info,output)
                
                todata_num,todata_data = todata
                todata_data = todata_data.replace('\0+', '')
                todata_data = todata_data.replace('\0-', '')
                todata_data = todata_data.replace('\0^', '')
                # todata_data = move_flag_to_behind(todata_data)
                todata_data = todata_data.replace('\1', '')
                # print('1{}'.format(todata_data))
                level = self._get_level(todata_data)
                # print('level为{}'.format(level))
                if todata_data != '\n' and todata_num != '':
                    if level == 0:
                        # if not to_all_info.get('global'):
                        #     to_all_info['global'] = {}
                        to_all_info[todata_data] = {}
                    else:
                        output,self.flag = self.get_true_before(text_a,todata_num-1,level, todata_data)
                        # print(output)
                        to_all_info  = self._merge_dicts(to_all_info,output)
        return from_all_info, to_all_info

    def dict_to_conf(self,dictionary):
        keys = []

        def recursive_keys(dictionary):
            for key, value in dictionary.items():
                keys.append(key)
                if isinstance(value, dict):
                    recursive_keys(value)

        recursive_keys(dictionary)
        return '\n'.join(keys)

    def main(self):
        diffs = difflib._mdiff(self.old_config, self.new_config)
        # print(diffs)
        from_all_info, to_all_info = self.collect_lines(diffs)
        print('from_all_info{}'.format(json.dumps(from_all_info,indent=2)))
        change_old_config = self.dict_to_conf(from_all_info)
        print('to_all_info{}'.format(json.dumps(to_all_info,indent=2)))
        change_new_config = self.dict_to_conf(to_all_info)
        print(change_new_config)
        print(change_old_config)
        change_new_lines = change_new_config.splitlines()
        change_old_lines = change_old_config.splitlines()
        # # 全量文字版对比
        d = difflib.Differ()
        diff = d.compare(change_new_lines, change_old_lines)
        differ = '\n'.join(list(diff))
        print(differ)
        return differ, from_all_info, to_all_info
