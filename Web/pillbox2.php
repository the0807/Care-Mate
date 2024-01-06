<html>
    <head>
        <meta charset="utf-8">
        <link href="css/btn.css" rel="stylesheet" type="text/css" />
        </style>
    </head>
    <body align="Center">
        <?php
            if(empty($_REQUEST["p_name"])) {
                $p_name ="";
            }
            else{
                $p_name =$_REQUEST["p_name"];
            }

            if(empty($_REQUEST["p_birthdate"])) {
                $p_birthdate ="";
            }
            else{
                $p_birthdate =$_REQUEST["p_birthdate"];
            }
        ?>
        <br><br><br>

        약통2에 환자를 지정하세요!
        <?php
            $conn1 = mysqli_connect('localhost', 'root', '11223344', 'Patient');
            if ( !$conn1 ) die('DB Error');

            $conn2 = mysqli_connect('localhost', 'root', '11223344', 'PillBox');
            if ( !$conn2 ) die('DB Error');

        ?>

        <br><br>
        <form class="" method="post" action="">
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 이름 : <input type="text" name="p_name" class="form-control" placeholder="홍길동" style="width:200px;height:40px;font-size:15px;" maxlength="4" autofocus><br><br>
        생년월일 : <input type="text" name="p_birthdate" class="form-control" placeholder="000807" style="width:200px;height:40px;font-size:15px;"  maxlength="6" autofocus>
        <br><button type="submit" class="btn-3d blue">약통 지정하기</button>
        <br></form>

        <?php
            $sql1 = "SELECT * FROM patient_info where P_NAME ='$p_name' and P_BIRTHDATE = '$p_birthdate'";
            $rs1 = mysqli_query($conn1, $sql1);
            $p_id = (mysqli_fetch_array($rs1))[P_ID];
            if ($p_name != "" && $p_id == NULL)
            {
                echo "환자 정보가 없습니다! <br>";
                echo "다시 입력하세요.";

            }
            else if ($p_name != "" && $p_id != NULL)
            {
                $sql2 = "INSERT INTO patient_info (P_ID, P_NAME, P_BIRTHDATE) VALUE ('$p_id', '$p_name', '$p_birthdate')";
                mysqli_query($conn2, $sql2);
                
                $sql3 = "UPDATE patient_pillbox SET P_ID = $p_id WHERE B_ID = 'PB_2'";
                mysqli_query($conn2, $sql3);

                echo "<script>location.href='index.php'</script>";
            }

            mysqli_close($conn1);
            mysqli_close($conn2);
        ?>


        <br><br><br><br>
        <div class="btn-container">
            <a href="index.php" class="btn-3d blue">메인페이지로 돌아가기</a>
        </div>
    </body>
</html>
