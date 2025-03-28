import React, { useEffect, useState } from 'react';
import CardDataStats from '../../components/CardDataStats';
import { BASE_URL } from '../../utils/urls';
import { Compyuter, InfoComputerData } from '../../types/compyuters';
import axioss from '../../api/axios';
import { isAuthenticated } from '../../utils/auth';
import { Navigate } from 'react-router-dom';
import { FaComputer } from "react-icons/fa6";
import { AiOutlinePrinter } from "react-icons/ai"
import { MdOutlineAdfScanner, MdSignalWifiStatusbarConnectedNoInternet2 } from "react-icons/md";
import { RiComputerLine, RiWebcamLine } from "react-icons/ri";
import ComputerTable from '../../components/Tables/DataTable';
import Skeleton from '../../components/Skeleton/Skeleton';
import { GrCloudComputer } from 'react-icons/gr';
import { TbFunctionFilled } from 'react-icons/tb';

const Main: React.FC = () => {
  const [data, setData] = useState<Compyuter[] | null>()
  const [computerData, setComputerData] = useState<Compyuter[]>([])
  const [selectKey, setSelectKey] = useState<string | null>("")
  const [deleteCompForChecked, setDeleteCompForChecked] = useState<boolean>(false)
  const [infoCompData, setInfoCompData] = useState<InfoComputerData | null>()
  const token = localStorage.getItem('token')

  useEffect(() => {
    if (!token) return
    axioss
      .get(`${BASE_URL}/all_compyuters/`)
      .then((response) => {
        setData(response.data);
      })
      .catch((err) => console.log(err));

    axioss
      .get(`${BASE_URL}/info-comp/`)
      .then((response) => {
        setInfoCompData(response.data);
      })
      .catch((err) => console.log(err));
  }, []);

  useEffect(() => {
    if (!selectKey) return;

    axioss
      .post(`${BASE_URL}/filter-data/`, { key: selectKey })
      .then((response) => {
        console.log("Serverdan kelgan ma'lumot:", response.data);
        setComputerData(response.data);
      })
      .catch((err) => console.log("Xatolik tafsilotlari:", err.response?.data));
  }, [selectKey, deleteCompForChecked]);

  console.log(infoCompData?.all_worked_compyuters_count);


  if (!isAuthenticated()) {
    return <Navigate to="/auth/signin" />
  }

  return (
    <>
      {data ?
        <>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 xl:grid-cols-4 2xl:gap-7.5">

            <CardDataStats title="Все компьютеры" total={`${infoCompData?.all_compyuters_count}`} setSelectKey={setSelectKey}>
              <FaComputer className="fill-primary dark:fill-white text-2xl" width="35" height="30" />
            </CardDataStats>

            <CardDataStats title="Рабочие компьютеры" total={`${infoCompData?.all_worked_compyuters_count}`} setSelectKey={setSelectKey}>
              <RiComputerLine className="fill-primary dark:fill-white text-2xl" width="35" height="30" />
            </CardDataStats>    
            
            <CardDataStats title="Не рабочие компьютеры" total={`${infoCompData?.all_noworked_compyuters_count}`} setSelectKey={setSelectKey}>
              <RiComputerLine className="fill-primary dark:fill-white text-2xl" width="35" height="30" />
            </CardDataStats>
        

            <CardDataStats title="Веб-камеры" total={`${infoCompData?.all_compyuters_with_webcam}`} setSelectKey={setSelectKey}>
              <RiWebcamLine className="fill-primary dark:fill-white text-2xl" width="35" height="30" />
            </CardDataStats>



            <CardDataStats title="Интернет" total={`${infoCompData?.all_compyuters_with_net}`} setSelectKey={setSelectKey}>
              <MdSignalWifiStatusbarConnectedNoInternet2 style={{ color: "#3C50E0" }} className="fill-primary dark:fill-white text-2xl" width="20" height="22" />
            </CardDataStats>

            <CardDataStats title="Принтеры" total={`${infoCompData?.all_compyuters_with_printer}`} setSelectKey={setSelectKey} >
              <AiOutlinePrinter className="fill-primary dark:fill-white text-2xl" width="35" height="30" />
            </CardDataStats>

            <CardDataStats title="Сканеры" total={`${infoCompData?.all_compyuters_with_scaner}`} setSelectKey={setSelectKey}>
              <MdOutlineAdfScanner className="fill-primary dark:fill-white text-2xl" width="35" height="30" />
            </CardDataStats>

            <CardDataStats title="МФУ" total={`${infoCompData?.all_compyuters_with_mfo}`} setSelectKey={setSelectKey}>
              <TbFunctionFilled style={{ color: "#3C50E0" }} className="fill-primary dark:fill-white text-2xl" width="35" height="30" />
            </CardDataStats>

          </div>

          <div className='mt-6'>
            {/* <MainTable /> */}
            <ComputerTable checkedComputer={computerData} setDeleteCompForChecked={setDeleteCompForChecked} />
          </div>
        </> :

        <div className='grid grid-cols-12'>
          <div className='col-span-3 '>
            <Skeleton />
          </div>
          <div className='col-span-3 '>
            <Skeleton />
          </div>
          <div className='col-span-3 '>
            <Skeleton />
          </div>
          <div className='col-span-3 '>
            <Skeleton />
          </div>

        </div>

      }


    </>
  );
};

export default Main;
