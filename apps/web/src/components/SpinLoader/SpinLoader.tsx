import { Spin, Flex } from "antd"
import { LoadingOutlined } from '@ant-design/icons';

const SpinLoader = () => {
    return <Flex justify="center" align="center" style={{ height: '100vh'}}>
        <Spin indicator={<LoadingOutlined style={{ fontSize: '24pt'}} />} />
    </Flex> 
}

export default SpinLoader